from langgraph.graph import StateGraph, END
from langchain_community.agent_toolkits import create_sql_agent
from .utils import connect_aws_db
from .prompt_manager import get_prompt
from .cilent import get_client

## 추후 수정예정
def build_car_recommendation_workflow():

    # 1. 사용자 입력 처리
    def process_user_input(data):
        user_input = data.get("user_input", "")
        return {"processed_input": user_input}

    # 2. 쿼리 생성 (LLM 사용)
    def generate_query(data):
        processed_input = data["processed_input"]
        
        # LangChain SQL Agent 생성
        db = connect_aws_db()
        agent = create_sql_agent(
            model=get_client(), 
            db=db, 
            agent_type="openai-tools", 
            verbose=True, 
            prompt=get_prompt()
        )
        
        # LLM을 사용해 SQL 쿼리 생성
        query = agent.invoke(processed_input)["output"]
        return {"generated_query": query}

    # 3. 데이터베이스 검색
    def execute_query(data):
        query = data["generated_query"]
        db = connect_aws_db()
        try:
            with db.connect() as conn:
                result = conn.execute(query).fetchall()
            return {"db_result": result}
        except Exception as e:
            return {"db_result": [], "error": str(e)}

    # 4. 결과 생성
    def generate_response(data):
        db_result = data.get("db_result", [])
        if not db_result:
            return {"response": "조건에 맞는 차량을 찾을 수 없습니다."}
        
        response = "추천 차량 리스트:\n"
        for row in db_result:
            response += f"- {row['name']} (특징: {row['features']})\n"
        return {"response": response}

    # 5. 종료 여부 결정
    def should_continue(data):
        if "종료" in data.get("processed_input", "").lower():
            return "end"
        return "continue"

    # LangGraph 워크플로 생성
    workflow = StateGraph(state_schema={})
    workflow.add_node("user_input", process_user_input)
    workflow.add_node("generate_query", generate_query)
    workflow.add_node("execute_query", execute_query)
    workflow.add_node("generate_response", generate_response)

    workflow.set_entry_point("user_input")  # 시작 지점 설정

    # 노드 연결
    workflow.add_edge("user_input", "generate_query")
    workflow.add_edge("generate_query", "execute_query")
    workflow.add_edge("execute_query", "generate_response")
    workflow.add_conditional_edges(
        "generate_response",
        should_continue,
        {"continue": "user_input", "end": END},
    )

    return workflow
