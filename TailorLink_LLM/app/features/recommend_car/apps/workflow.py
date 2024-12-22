from langgraph.graph import StateGraph, END, START
from langchain_community.agent_toolkits import create_sql_agent
from app.features.recommend_car.apps.utils import connect_aws_db, parse_milvus_results
from app.features.recommend_car.apps.prompt_manager import get_prompt, get_suggest_question_prompt, get_system_prompt
from app.features.recommend_car.apps.cilent import get_client
from app.features.recommend_car.apps.agent_state import AgentState
from app.features.recommend_car.apps.database.milvus_connector import client, generate_kobert_embedding
from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import SystemMessage, HumanMessage
from typing import Sequence
from pymilvus.model.reranker import CrossEncoderRerankFunction
import json 

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
            response = client([system_prompt, human_message])  # 메시지 배열로 전달
            state["response"] = response.content.strip()
        except Exception as e:
            state["response"] = "모델 호출에 실패했습니다. 다시 시도해주세요."
            print(f"[ERROR] LLM 호출 실패: {e}")

        return state

    def generate_query(state: AgentState):
        """
        사용자 입력에 기반한 SQL 쿼리 실행
        """
        inputs = state["user_input"]
        db = connect_aws_db()
        agent = create_sql_agent(
            llm=get_client(),
            db=db,
            agent_type="openai-tools",
            verbose=True,
            prompt=get_prompt(),
        )
        try:
            # 모델 호출
            result = agent.invoke(inputs)["output"]
            print(f"[DEBUG] Agent Response: {result}")

            state["db_result"] = result
        except Exception as e:
            print(f"[ERROR] 쿼리 생성 실패: {e}")

        return state

    def milvus_search(state: AgentState):
        query = state.get("user_input", "")
        query_vector = generate_kobert_embedding(query)
        try:
            search_results = client.search(
                collection_name="genesis",
                data=[query_vector],
                anns_field="vector",
                search_params={"metric_type": "L2", "params": {"nprobe": 10}},
                limit=3,
            )
            state["milvus_result"] = parse_milvus_results(search_results)
        except Exception as e:
            state["milvus_result"] = []
            print(f"[ERROR] Milvus 검색 실패: {e}")
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
            state["final_result"] = []
            state["response"] = (
                f"{result_status}. 죄송합니다. 조건을 수정하거나 추가 정보를 제공해 주세요."
            )
            return state

        try:
            ce_rf = CrossEncoderRerankFunction(
                        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2",  
                        device="cpu"
            )

            db_text = f"DB 결과: {db_results[0].get('car_name', '정보 없음')}" if db_results else "DB 결과 없음"

            # Milvus 결과를 문장으로 변환 
            milvus_text = f"차량 ID {milvus_results.get('car_id')}, {milvus_results.get('metadata')}"

            # Reranking 수행
            reranked_results = ce_rf(
                query=state["user_input"],
                documents=[db_text, milvus_text],
                top_k=1
            )
            # Re-ranking 결과를 state에 저장
            state["final_result"] = reranked_results
            print("[DEBUG] Re-ranking 결과:", reranked_results)  

        except Exception as e:
            print(f"[ERROR] Re-ranking 실패: {e}")
            state["final_result"] = []

        return state

    def suggest_question_node(state: AgentState):
        """
        예상 질문 생성 노드
        """
        final_results = state.get("final_result", [])
        if not final_results:
            state["suggested_questions"] = []
            return state

        # 첫 번째 결과에서 car_name과 features 가져오기
        top_result = final_results[0]
        features = top_result.get("metadata", "").strip()

        # 예상 질문을 생성하는 LLM 프롬프트 작성
        prompt = get_suggest_question_prompt(features)

        try:
            # LLM 호출 및 예상 질문 생성
            llm_response = get_client().invoke(prompt)
            suggested_questions = [
                line.strip() for line in llm_response.split("\n") if line.strip()
            ]
            state["suggested_questions"] = suggested_questions[:3]  # 최대 3개의 질문 저장
        except Exception as e:
            print(f"[ERROR] 예상 질문 생성 중 오류 발생: {e}")
            state["suggested_questions"] = []

        return state

    def generate_response(state: AgentState):
        """
        최종 응답 생성: 최상위 차량 하나만 반환
        """
        final_results = state.get("final_result", [])
        if not final_results:
            return state

        # 상위 한 개의 차량만 사용
        top_car = final_results[0]
        features = top_car.get("metadata", "특징 정보 없음")
        # 응답 메시지 생성
        state["response"] = f"추천 차량:\n- {features["car_name"]} (특징: {features})"
        return state

    def route_based_on_response(state: AgentState) -> Sequence[str]:
        """
        모델 응답을 기반으로 경로를 결정.
        """
        response = state.get("response", "").lower()

        # 검색 불필요 조건
        if "제네시스 외의 차량은 추천할 수 없습니다" in response or "조건에 맞는 차량을 찾지 못했습니다" in response:
            print("[DEBUG] 모델 응답: 검색 불필요")
            return ["generate_response"]

        # 추가 정보 요청
        elif "추천을 위해 예산" in response or "사용 목적 등을 알려주세요" in response:
            print("[DEBUG] 모델 응답: 추가 정보 요청")
            return ["generate_response"]

        # 예외 처리
        else:
            print("[DEBUG] 모델 응답: 검색 필요")
            return ["generate_query"]

    def analyze_results(db_results, milvus_results):
        """
        DB 및 Milvus 결과를 분석하여 상태를 반환.
        """
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
            state["response"] = (
                "조건에 맞는 차량을 찾지 못했습니다. "
                "예산, 차량 종류, 사용 목적 등의 정보를 다시 확인해 주세요."
            )
            return ["generate_response"]

        print(f"[DEBUG] {result_status}: rerank_node로 이동")
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
        ["rerank_node", "generate_response"],  # 조건에 따라 rerank_node 또는 generate_response로 이동
    )   
    workflow.add_edge("rerank_node", "suggest_question")  # Re-ranking 후 예상 질문 생성
    workflow.add_edge("suggest_question", "generate_response")  # 예상 질문 생성 후 응답 생성
    workflow.add_edge("generate_response", END)

    # 컴파일된 워크플로우 반환
    return workflow.compile(checkpointer=memory_saver)
