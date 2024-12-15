
from langchain_openai import ChatOpenAI

# 모델(LLM) 을 생성합니다.
def get_OpenAI(model_name="gpt-4o-mini"):
    llm = ChatOpenAI(model_name=model_name, temperature=0)
    return llm
