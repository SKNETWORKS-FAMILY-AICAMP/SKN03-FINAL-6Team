from langgraph.graph import StateGraph, END, START
from langchain_community.agent_toolkits import create_sql_agent
from .utils import connect_aws_db, rerank_results
from .prompt_manager import get_prompt, get_suggest_question_prompt, get_system_prompt
from .cilent import get_client
from .agent_state import AgentState
from recommend_car.apps.database.milvus_connector import client, generate_kobert_embedding
from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import SystemMessage, HumanMessage
from typing import Sequence
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
        사용자 입력에 기반한 SQL 쿼리 생성
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
            query = agent.invoke(inputs)["output"]
            state["generated_query"] = query
        except Exception as e:
            state["generated_query"] = ""
            state["error"] = f"쿼리 생성 실패: {e}"
            print(f"[ERROR] 쿼리 생성 실패: {e}")

        return state

    def execute_query(state: AgentState):
        """
        데이터베이스에서 쿼리 실행
        """
        query = state.get("generated_query", "")
        if not query:
            state["db_result"] = []
            state["error"] = "쿼리가 비어 있습니다."
            return state

        db = connect_aws_db()  # SQLDatabase 객체
        try:
            # SQLDatabase의 run 메서드를 사용하여 쿼리 실행
            result = db.run(query)
            state["db_result"] = result  # run 메서드 결과를 그대로 사용
        except Exception as e:
            state["db_result"] = []
            state["error"] = f"DB 검색 실패: {e}"
            print(f"[ERROR] DB 검색 실패: {e}")

        return state

    def milvus_search(state: AgentState):
        """
        Milvus에서 유사도 기반 검색 수행
        """
        query = state.get("user_input", "")
        query_vector = generate_kobert_embedding(query)

        try:
            search_results = client.search(
                collection_name="genesis",
                data=[query_vector],
                anns_field="vector",
                search_params={"metric_type": "L2", "params": {"nprobe": 10}},
                limit=10,
            )
            parsed_results = [
                {
                    "car_id": str(hit.get("id")),
                    "car_name": hit.get("car_name"),
                    "score": hit.get("distance"),
                }
                for result_list in search_results
                for hit in result_list
            ]
            state["milvus_result"] = parsed_results
        except Exception as e:
            state["milvus_result"] = []
            state["error"] = f"Milvus 검색 실패: {e}"
            print(f"[ERROR] Milvus 검색 실패: {e}")

        return state

    def rerank_node(state: AgentState):
        """
        Re-ranking 결과 생성
        """
        db_results = state.get("db_result", [])
        milvus_results = state.get("milvus_result", [])

        if not db_results and not milvus_results:
            state["final_result"] = []
            return state

        state["final_result"] = rerank_results(
            db_results=db_results, milvus_results=milvus_results, weights=[0.6, 0.4]
        )
        return state

    def generate_response(state: AgentState):
        """
        최종 응답 생성
        """
        final_results = state.get("final_result", [])
        if not final_results:
            return state

        response = "추천 차량 리스트:\n"
        for car in final_results:
            car_name = car.get("car_name", "알 수 없음")
            features = car.get("features", "")
            response += f"- {car_name} (특징: {features})\n"
        state["response"] = response.strip()

        return state

    def route_based_on_response(state: AgentState) -> Sequence[str]:
        """
        응답에 따라 경로 결정
        """
        response = state.get("response", "")
        if "죄송" in response:
            return ["generate_response"]
        return ["generate_query"]

    def has_valid_results(results):
        """
        결과 리스트에서 유효한 car_name이 있는지 확인
        """
        return any(result.get("car_name") for result in results)

    def route_based_on_results(state: AgentState) -> Sequence[str]:
        """
        DB 및 Milvus 결과에 따라 경로 결정:
        - 유효한 결과가 없으면 generate_response로 이동.
        - 유효한 결과가 있으면 rerank_node로 이동.
        """
        db_results = state.get("db_result", [])
        milvus_results = state.get("milvus_result", [])

        # DB 및 Milvus 결과 유효성 검사
        db_has_valid_results = has_valid_results(db_results)
        milvus_has_valid_results = has_valid_results(milvus_results)

        if not db_has_valid_results and not milvus_has_valid_results:
            print("[DEBUG] DB와 Milvus 결과가 유효하지 않아 generate_response로 이동")
            return ["generate_response"]

        print("[DEBUG] DB 또는 Milvus 결과가 유효하므로 rerank_node로 이동")
        return ["rerank_node"]



    # Workflow 정의
    workflow = StateGraph(state_schema=AgentState)

    # 노드 추가
    workflow.add_node("input_process", process_user_input)
    workflow.add_node("generate_query", generate_query)
    workflow.add_node("execute_query", execute_query)
    workflow.add_node("milvus_search", milvus_search)
    workflow.add_node("rerank_node", rerank_node)
    workflow.add_node("generate_response", generate_response)

    # 노드 연결
    workflow.add_edge(START, "input_process")
    workflow.add_conditional_edges(
        "input_process", route_based_on_response, ["generate_query", "generate_response"]
    )
    workflow.add_edge("generate_query", "execute_query")
    workflow.add_edge("execute_query", "milvus_search")
    workflow.add_conditional_edges(
        "milvus_search",
        route_based_on_results,
        ["rerank_node", "generate_response"],  # 조건에 따라 rerank_node 또는 generate_response로 이동
    )   
    workflow.add_edge("rerank_node", "generate_response")
    workflow.add_edge("generate_response", END)

    # 컴파일된 워크플로우 반환
    return workflow.compile(checkpointer=memory_saver)
