from langgraph.graph import StateGraph, END, START
from langchain_community.agent_toolkits import create_sql_agent
from .utils import connect_aws_db, rerank_results
from .prompt_manager import get_prompt, get_suggest_question_prompt
from .cilent import get_client
from .agent_state import AgentState
from recommend_car.apps.database.milvus_connector import client, generate_kobert_embedding
from langgraph.checkpoint.memory import MemorySaver
import json 

def has_final_results(state: AgentState):
    """
    조건부 실행을 위한 함수: final_results 존재 여부 확인
    """
    return state.get("final_result", []) is not None  # None이 아니면 True 반환


def build_car_recommendation_workflow():
    # LangGraph MemorySaver 초기화
    memory_saver = MemorySaver()

    # 1. 사용자 입력 처리
    def process_user_input(state: AgentState):
        user_input = state["user_input"]
        return {"processed_input": user_input}

    # 2. 쿼리 생성 (LLM 사용)
    def generate_query(state: AgentState):
        processed_input = state["processed_input"]
        db = connect_aws_db()
        agent = create_sql_agent(
            llm=get_client(),
            db=db,
            agent_type="openai-tools",
            verbose=True,
            prompt=get_prompt()
        )
        query = agent.invoke(processed_input)["output"]
        return {"generated_query": query}

    # 3. 데이터베이스 검색
    def execute_query(state: AgentState):
        query = state["generated_query"]
        db = connect_aws_db()
        try:
            with db.connect() as conn:
                result = conn.execute(query).fetchall()
            return {"db_result": result}
        except Exception as e:
            return {"db_result": [], "error": str(e)}

    # 4. Milvus 검색
    def milvus_search(state: AgentState):
        """
        Milvus에서 유사도 기반 검색을 수행하는 노드
        """
        query = state["user_input"]
        query_vector = generate_kobert_embedding(query)

        search_results = client.search(
            collection_name="genesis",
            data=[query_vector],
            anns_field="vector",
            search_params={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=10
        )
        print(f"Milvus 검색 결과: {search_results}")

        parsed_results = []
        try:
            if search_results and isinstance(search_results, list):
                for result_list in search_results:  # Milvus 결과의 첫 번째 리스트 처리
                    if isinstance(result_list, list):  # 내부 리스트 확인
                        for hit in result_list:  # 내부 리스트 처리
                            parsed_results.append({
                                "car_id": hit.get("id", "unknown"),
                                "car_name": "알 수 없는 차량",
                                "score": hit.get("distance", 100.0)
                            })
            else:
                print("[WARNING] 예상과 다른 검색 결과 구조입니다:", search_results)
        except Exception as e:
            print(f"[ERROR] Milvus 결과 파싱 중 오류 발생: {e}")

        if not parsed_results:
            print("Milvus 결과가 비어 있습니다. 기본값으로 설정합니다.")
            parsed_results = [{"car_id": "unknown", "car_name": "알 수 없는 차량", "score": 100.0}]

        print("파싱된 Milvus 결과:", parsed_results)
        return {"milvus_result": parsed_results}

    # 5. Re-ranking 수행
    def rerank_node(state: AgentState):
        db_results = state.get("db_result", [])
        milvus_results = state.get("milvus_result", [])

        # 빈 결과 처리
        if not db_results and not milvus_results:
            print("Re-ranking 노드: DB 및 Milvus 결과가 모두 비어 있습니다.")
            return {"final_result": []}

        # Re-ranking 수행
        final_results = rerank_results(
            db_results=db_results, 
            milvus_results=milvus_results, 
            weights=[0.6, 0.4]
        )
        print("[DEBUG] Re-ranking 완료 결과:", final_results)
        return {"final_result": final_results}


    # 6. 결과 생성
    def generate_response(state: AgentState):
        """
        결과 생성 노드
        """
        final_results = state.get("final_result", [])
        print("[DEBUG] rerank_node -> final_result:", state.get("final_result", []))
        if not final_results:
            response = "조건에 맞는 차량을 찾을 수 없습니다."
        else:
            response = "추천 차량 리스트:\n"
            for car in final_results:
                car_name = car.get('car_name')
                features = car.get('features', '')
                # car_name이 없으면 해당 항목은 무시
                if not car_name or car_name == "알 수 없는 차량":
                    continue
                response += f"- {car_name} (특징: {features})\n"

            # 결과가 완전히 비어있는 경우 처리
            if response.strip() == "추천 차량 리스트:":
                response = "조건에 맞는 차량을 찾을 수 없습니다."
        return {"response": response}

    # 7. 예상 질문 생성
    def suggest_question_node(state: AgentState):
        """
        예상 질문 생성 노드
        """
        final_results = state.get("final_result", [])
        if not final_results:
            return {"suggest_question": []}

        # 첫 번째 결과에서 car_name이 비어있으면 질문 생성 생략
        top_result = final_results[0]
        car_name = top_result.get("car_name", "").strip()
        features = top_result.get("features", "").strip()

        if not car_name or car_name == "알 수 없는 차량":
            print("[DEBUG] 예상 질문 생략: car_name이 비어 있습니다.")
            return {"suggest_question": []}

        prompt = get_suggest_question_prompt(car_name, features)

        try:
            llm_response = get_client().invoke(prompt)
            suggest_question = [line.strip() for line in llm_response.split("\n") if line.strip()]
            return {"suggest_question": suggest_question[:3]}
        except Exception as e:
            print(f"[ERROR] 예상 질문 생성 중 오류 발생: {e}")
            return {"suggest_question": []}

    # Workflow 정의
    workflow = StateGraph(state_schema=AgentState)

    # 노드 추가
    workflow.add_node("input_process", process_user_input)
    workflow.add_node("generate_query", generate_query)
    workflow.add_node("execute_query", execute_query)
    workflow.add_node("milvus_search", milvus_search)
    workflow.add_node("rerank_node", rerank_node)
    workflow.add_node("suggest_question", suggest_question_node)
    workflow.add_node("generate_response", generate_response)

    # 노드 연결
    workflow.add_edge(START, "input_process")
    workflow.add_edge("input_process", "generate_query")
    workflow.add_edge("generate_query", "execute_query")
    workflow.add_edge("execute_query", "milvus_search")
    workflow.add_edge("milvus_search", "rerank_node")
    workflow.add_edge("rerank_node", "generate_response")  

    workflow.add_conditional_edges(
        "rerank_node",
        {
            "suggest_question": lambda state: bool(state.get("final_result", [])),  # 결과가 있으면 suggest_question 실행
            "generate_response": lambda state: not bool(state.get("final_result", []))  # 결과 없으면 바로 generate_response
        }
    )

    # suggest_question 실행 후 generate_response로 이동
    workflow.add_edge("suggest_question", "generate_response")

    # generate_response → END
    workflow.add_edge("generate_response", END)

    # 메모리 설정
    memory_saver = MemorySaver()  # 메모리 초기화

    # 컴파일된 워크플로우 반환
    compiled_workflow = workflow.compile(checkpointer=memory_saver) 
    return compiled_workflow

def log_condition(branch_name, condition_result):
    print(f"[DEBUG] Condition Check: {branch_name}, Result: {condition_result}")
    return condition_result