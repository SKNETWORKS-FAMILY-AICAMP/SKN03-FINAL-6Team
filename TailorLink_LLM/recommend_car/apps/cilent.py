from langchain_openai import ChatOpenAI

def get_client(model_id: str = "gpt-4o-mini"):
    try:
        return ChatOpenAI(model=model_id, temperature=0)
    except Exception as e:
        return (f"ChatOpenAI를 불러오지 못했습니다.: {e}")
