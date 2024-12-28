from langgraph.graph import StateGraph, END, START
from app.features.recommend_car.apps.utils import connect_aws_db, parse_milvus_results, extract_json_from_text
from app.features.recommend_car.apps.prompt_manager import get_prompt, get_suggest_question_prompt, get_system_prompt, get_suggest_recommend_style_prompt
from app.features.recommend_car.apps.cilent import get_client
from app.features.recommend_car.apps.agent_state import AgentState
from app.features.recommend_car.apps.database.milvus_connector import client, generate_kobert_embedding
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from typing import Sequence
from pymilvus.model.reranker import CrossEncoderRerankFunction
import ast

def build_car_recommendation_workflow():
    # LangGraph MemorySaver 초기화
    memory_saver = MemorySaver()

    def process_user_input(state: AgentState):
        """
        사용자 입력 처리 및 모델 응답 저장
        """
        inputs = state.get("user_input", "")
        if isinstance(inputs, list):  # 입력값이 리스트인 경우 첫 번째 값만 사용
            inputs = inputs[0]
        elif not isinstance(inputs, str):  # 문자열이 아닌 경우 기본값으로 변환
            inputs = str(inputs)

        state["user_input"] = inputs.strip()  # 공백 제거 후 저장

        # 시스템 프롬프트와 사용자 메시지 생성
        system_prompt = SystemMessage(content=get_system_prompt())
        human_message = HumanMessage(content=inputs)

        # LLM 호출
        client = get_client()
        try:
            # 모델 호출
            response = client.invoke([system_prompt, human_message])
            full_response = response.content.strip()

            # 응답, 의도, 조건 분리
            if "응답:" in full_response and "의도:" in full_response and "조건:" in full_response:
                response_part = full_response.split("의도:")[0].replace("응답:", "").strip()
                intent_part = full_response.split("의도:")[1].split("조건:")[0].strip()
                conditions = full_response.split("조건:")[1].strip().split(", ")
            else:
                response_part = full_response
                intent_part = "미확인"
                conditions = []

            # 상태 업데이트
            state["response"] = response_part
            print("응답!!!! :" + response_part)
            state["intent"] = intent_part
            state["conditions"] = conditions

            print(f"[DEBUG] Detected intent: {state['intent']}")
            print(f"[DEBUG] Extracted conditions: {conditions} (Count: {len(conditions)})")

        except Exception as e:
            state["response"] = "모델 호출에 실패했습니다. 다시 시도해주세요."
            state["intent"] = "오류"
            state["conditions"] = []
            print(f"[ERROR] LLM 호출 실패: {e}")

        return state  # 반드시 업데이트된 state를 반환

    
    def generate_query(state: AgentState):
        """
        사용자 입력에 기반한 SQL 쿼리 실행 후 JSON 형식의 결과만 추출
        """
        inputs = state["user_input"]
        db = connect_aws_db()
        toolkit = SQLDatabaseToolkit(db=db, llm=get_client())
        agent_executor = create_react_agent(
            get_client(), 
            toolkit.get_tools(), 
            state_modifier=get_prompt()
        )
        try:
            events = agent_executor.invoke(
                {"messages": [("user", inputs)]}
            )
            messages = events.get("messages")
            # 최종 AIMessage의 content 추출
            final_message = None
            for message in reversed(messages):
                if isinstance(message, AIMessage) and message.content:
                    final_message = message.content
                    break

            # 결과 출력
            if final_message:
                result = extract_json_from_text(final_message)
                print(f"[DEBUG] 추출된 JSON: {result}")
                state["db_result"] = result
            else:
                print("AIMessage with content not found.")
        except Exception as e:
            print(f"[ERROR] 쿼리 생성 실패: {e}")
            state["db_result"] = None
        return state

    def milvus_search(state: AgentState):
        query = state.get("user_input", "")
        query_vector = generate_kobert_embedding(query)
        try:
            search_results = client.search(
                collection_name="genesis",
                data=[query_vector],
                limit=3,
                output_fields=["car_id", "$meta"]
            )
            print("[DEBUG] Milvus 검색 결과:", search_results)
            state["milvus_result"] = parse_milvus_results(search_results)
        except Exception as e:
            state["milvus_result"] = []
            print(f"[ERROR] Milvus 검색 실패: {str(e)}")
            print(f"[DEBUG] 예외 args: {e.args}")  # 예외 메시지 상세 정보 출력
        return state

    def rerank_node(state: AgentState):
        """
        DB와 Milvus 검색 결과를 Re-ranking.
        """
        db_results = state.get("db_result", [])
        milvus_results = state.get("milvus_result", [])

        # 결과 유효성 검증
        result_status, is_valid = analyze_results(db_results, milvus_results)

        if not is_valid:
            print(f"[ERROR] Re-ranking 불가: {result_status}")
            state["final_result"] = {}
            state["response"] = (
                f"{result_status}. 죄송합니다. 조건을 수정하거나 추가 정보를 제공해 주세요."
            )
            return state

        try:
            print("[DEBUG] rerank node 진입")
            ce_rf = CrossEncoderRerankFunction(
                        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",
                        device="cpu"
            )

            db_text = (
                f"차량 ID: {db_results[0]['car_id']} , 차량 Name: {db_results[0]['car_name']}, 차량 Image: {db_results[0]['car_image']}" if db_results and isinstance(db_results[0], dict) else "DB 결과 없음"
            )

            # Milvus 결과를 문장으로 변환
            print("[DEBUG] milvus_text 진입")
            milvus_text = (
                f"차량 ID {milvus_results[0]['car_id']}, {milvus_results[0].get('metadata', '정보 없음')}"
                if milvus_results and isinstance(milvus_results[0], dict) else "Milvus 결과 없음"
            )

            # Reranking 수행
            reranked_results = ce_rf(
                query=state["user_input"],
                documents=[db_text, milvus_text],
                top_k=1
            )
            # Re-ranking 결과를 state에 저장
            print("[DEBUG] Raw text:", reranked_results[0].text)  # 첫 번째 결과의 text 속성 접근
            raw_text = reranked_results[0].text
            data_start = raw_text.find("{")
            raw_dict_string = raw_text[data_start:]
            
            # Python 딕셔너리로 변환
            feature = ast.literal_eval(raw_dict_string)
            
            # 결과 출력
            print("[DEBUG] JSON 데이터:", feature)
            state["final_result"] = feature
            print("[DEBUG] Re-ranking 결과:", feature)

        except Exception as e:
            print(f"[ERROR] Re-ranking 실패: {e}")
            print(f"[DEBUG] 예외 타입: {type(e)}, 예외 args: {e.args}")
            state["final_result"] = []

        return state

    def suggest_question_node(state: AgentState):
        """
        예상 질문 생성 노드
        """
        final_result = state.get("final_result", {})
        if not final_result:
            state["suggested_questions"] = []
            return state

        # 첫 번째 결과에서 car_name과 features 가져오기
        top_result = final_result
        car_name = top_result.get("car_name", "").strip()
        features = top_result.get("car_info", "").strip()

        # 예상 질문을 생성하는 LLM 프롬프트 작성
        prompt = get_suggest_question_prompt(car_name, features)

        try:
            # LLM 호출 및 예상 질문 생성
            llm_response = get_client().invoke(prompt)
            response_text = llm_response.content  # 텍스트 내용 추출
            suggested_questions = [
                line.strip() for line in response_text.split("\n") if line.strip()
            ]
            state["suggested_questions"] = suggested_questions[:3]  # 최대 3개의 질문 저장
        except Exception as e:
            print(f"[ERROR] 예상 질문 생성 중 오류 발생: {e}")
            state["suggested_questions"] = []

        return state

    def generate_response(state: AgentState):
        """
        최종 응답 생성
        """
        final_result = state.get("final_result", [])
        intent = state.get("intent", "").lower()
        conditions = state.get("conditions", [])
        condition_count = len(conditions)
        final_result = state.get("final_result", {})
        if not final_result:
            print("[DEBUG] 결과값이 없습니다.")

            # 의도에 따른 분기 처리
            if "차량 추천" in intent:
                if condition_count < 2:
                    state["response"] = (
                        "추천을 위해 최소 2가지 이상의 조건이 필요합니다. "
                        "예를 들어, '(본인의 예산범위, 예산)에 해당되는 검은색 suv의 좋은 차량' 같은 요청을 해 주세요!"
                    )
                else:
                    state["response"] = (
                        "조건에 맞는 차량을 찾지 못했습니다. "
                        "다른 조건으로 다시 시도해 주세요!"
                    )

            return state

        # 상위 한 개의 차량만 사용
        top_car = final_result
        features = top_car.get("car_info", "특징 정보 없음")
        # 응답 메시지 생성
        car_name = top_car["car_name"]
        response = get_client().invoke(get_suggest_recommend_style_prompt(car_name, features))
        response_text = response.content
        state["response"] = response_text
        return state

    def route_based_on_response(state: AgentState) -> Sequence[str]:
        """
        모델 응답 및 입력 의도를 기반으로 경로를 결정.
        """
        intent = state.get("intent", "")
        conditions = state.get("conditions", [])
        condition_count = len(conditions)

        if "차량 추천" in intent:
            if condition_count >= 2:  # 조건이 2가지 이상인 경우
                print("[DEBUG] Intent: 차량 추천 (DB 및 Milvus 검색 수행)")
                return ["generate_query"]
            else:  # 조건이 1가지 이하인 경우
                print("[DEBUG] Intent: 차량 추천 (추가 정보 요청 필요)")
                return ["generate_response"]

        elif "추가 정보 요청" in intent:
            print("[DEBUG] Intent: 추가 정보 요청")
            return ["generate_response"]

        else:
            print("[DEBUG] Intent: 기타")
            return ["generate_response"]


    def analyze_results(db_results, milvus_results):
        # DB와 Milvus 결과가 모두 비어 있는 경우
        if not db_results and not milvus_results:
            return "DB와 Milvus 모두 결과 없음", False

        # DB 결과만 없는 경우
        if not db_results:
            return "DB 결과 부족", False

        # Milvus 결과만 없는 경우
        if not milvus_results:
            return "Milvus 결과 부족", False

        # Milvus 결과에 유효한 데이터가 없는 경우
        if all(result.get("car_id") is None and result.get("metadata") is None for result in milvus_results):
            return "Milvus 결과에 유효한 데이터 없음", False

        # 결과 있음
        return "결과 있음", True


    def route_based_on_results(state: AgentState) -> Sequence[str]:
        """
        DB 및 Milvus 결과 유무에 따라 경로를 결정.
        """
        db_results = state.get("db_result", [])
        milvus_results = state.get("milvus_result", [])

        # 결과 분석
        result_status, is_valid = analyze_results(db_results, milvus_results)

        if not is_valid:
            print(f"[DEBUG] {result_status}: generate_response로 이동")
            return ["generate_response"]

        return ["rerank_node"]

    # Workflow 정의
    workflow = StateGraph(state_schema=AgentState)

    # 노드 추가
    workflow.add_node("input_process", process_user_input)
    workflow.add_node("generate_query", generate_query)
    workflow.add_node("milvus_search", milvus_search)
    workflow.add_node("rerank_node", rerank_node)
    workflow.add_node("suggest_question", suggest_question_node)
    workflow.add_node("generate_response", generate_response)

    # 노드 연결
    workflow.add_edge(START, "input_process")
    workflow.add_conditional_edges(
        "input_process", route_based_on_response, ["generate_query", "generate_response"]
    )
    workflow.add_edge("generate_query", "milvus_search")
    workflow.add_conditional_edges(
        "milvus_search",
        route_based_on_results,
        ["rerank_node", "generate_response"], 
    )
    workflow.add_edge("rerank_node", "suggest_question")  # Re-ranking 후 예상 질문 생성
    workflow.add_edge("suggest_question", "generate_response")  # 예상 질문 생성 후 응답 생성
    workflow.add_edge("generate_response", END)

    # 컴파일된 워크플로우 반환
    return workflow.compile(checkpointer=memory_saver)