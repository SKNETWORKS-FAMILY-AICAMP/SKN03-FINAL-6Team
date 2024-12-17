from langgraph.graph import StateGraph, END, START
from langchain_community.agent_toolkits import create_sql_agent
from .utils import connect_aws_db, rerank_results
from .prompt_manager import get_prompt
from .cilent import get_client
from .agent_state import AgentState
from recommend_car.apps.database.milvus_connector import client, generate_kobert_embedding
## 추후 수정예정
def build_car_recommendation_workflow():
    # 1. 사용자 입력 처리   
    def process_user_input(AgentState):
        user_input = AgentState["user_input"]
        return {"processed_input": user_input}

    # 2. 쿼리 생성 (LLM 사용)
    def generate_query(AgentState):
        processed_input = AgentState["processed_input"]
        
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
    def execute_query(AgentState):
        query = AgentState["generated_query"]
        db = connect_aws_db()
        try:
            with db.connect() as conn:
                result = conn.execute(query).fetchall()
            return {"db_result": result}
        except Exception as e:
            return {"db_result": [], "error": str(e)}
            
    # 4. rerank 추천 노드
    def milvus_search(AgentState):
        """
        Milvus에서 유사도 기반 검색을 수행하는 노드
        """
        query = AgentState["user_input"]
        query_vector = generate_kobert_embedding(query)

        # Milvus 검색 수행
        search_results = client.search(
            collection_name="genesis",
            data=[query_vector],
            anns_field="vector",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=10
        )
        return {"milvus_result": search_results}

    # 5. rerank 추천 노드
    def rerank_node(AgentState):
        db_results = AgentState["db_result"]
        milvus_results = AgentState["milvus_result"]

        # Re-ranking 수행
        final_results = rerank_results(db_results, milvus_results, strategy="weighted", weights=[0.6, 0.4])
        return {"final_result": final_results}

    # 6 결과 생성
    def generate_response(AgentState):
        db_result = AgentState.get("db_result", [])
        if not db_result:
            return {"response": "조건에 맞는 차량을 찾을 수 없습니다."}
        
        response = "추천 차량 리스트:\n"
        for row in db_result:
            response += f"- {row['name']} (특징: {row['features']})\n"
        return {"response": response}

    #독립적인 노드
    def suggest_question(memory):
        question_list = []
        prompt = f"{memory}를 참고해서 예상 질문 3가지를 생성해주세요"        
        try:
            response = get_client(prompt)
            question_list = response.split("\n")[:3]
            return [q.strip() for q in question_list if q.strip()]
        except Exception as e:
            print(f"[ERROR] 예상 질문을 생성하는 중 오류 발생: {e}")
            return []
    
    # LangGraph 워크플로 생성
    workflow = StateGraph(state_schema=AgentState)
    workflow.add_node("input_process", process_user_input)
    workflow.add_node("generate_query", generate_query)
    workflow.add_node("execute_query", execute_query)
    workflow.add_node("milvus_search", milvus_search)
    workflow.add_node("rerank_node", rerank_node)
    workflow.add_node("generate_response", generate_response)

    # 노드 연결
    workflow.add_edge(START, "input_process")
    workflow.add_edge("input_process", "generate_query")
    workflow.add_edge("generate_query", "execute_query")
    workflow.add_edge("execute_query", "milvus_search")  # Milvus 검색 추가
    workflow.add_edge("milvus_search", "rerank_node")
    workflow.add_edge("rerank_node", "generate_response")
    workflow.add_edge("generate_response", END)
    return workflow
