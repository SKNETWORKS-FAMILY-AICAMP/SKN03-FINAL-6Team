from pydantic import BaseModel

class AgentState(BaseModel):
    user_input: str = None
    processed_input: str = None
    generated_query: str = None
    db_result: list = []
    milvus_result: list = []
    final_result: list = []
    response: str = None