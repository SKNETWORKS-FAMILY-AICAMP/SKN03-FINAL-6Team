from langgraph.graph import StateGraph, END, START
from langchain_community.agent_toolkits import create_sql_agent
from .utils import connect_aws_db, parse_milvus_results
from .prompt_manager import get_prompt, get_suggest_question_prompt, get_system_prompt
from .cilent import get_client
from .agent_state import AgentState
from recommend_car.apps.database.milvus_connector import client, generate_kobert_embedding
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
            print(f"[Debug 확인: {response.content.strip()}]")
        except Exception as e:
            state["response"] = "모델 호출에 실패했습니다. 다시 시도해주세요."
            print(f"[ERROR] LLM 호출 실패: {e}")

        return state

    def suggest_question_node(state: AgentState):
        """
        예상 질문 생성 노드
        """
        final_results = state["response"]
        print(f"[Debug 확인: {final_results}]")

        # # 첫 번째 결과에서 car_name과 features 가져오기
        # top_result = final_results[0]
        features = final_results.strip()
        if "추천을 위해 추가 정보" in final_results or "특별한 요구사항" in final_results:
            print("[DEBUG] 모델 응답: 추가 정보 요청")
            return ["generate_response"]
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
        features = state["response"]
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
            return ["suggest_question"]


    # Workflow 정의
    workflow = StateGraph(state_schema=AgentState)

    # 노드 추가
    workflow.add_node("input_process", process_user_input)
    workflow.add_node("suggest_question", suggest_question_node)  
    workflow.add_node("generate_response", generate_response)

    # 노드 연결
    workflow.add_edge(START, "input_process")
    workflow.add_conditional_edges(
        "input_process", route_based_on_response, ["suggest_question", "generate_response"]
    )
    workflow.add_edge("suggest_question", "generate_response")  # 예상 질문 생성 후 응답 생성
    workflow.add_edge("generate_response", END)

    # 컴파일된 워크플로우 반환
    return workflow.compile(checkpointer=memory_saver)
