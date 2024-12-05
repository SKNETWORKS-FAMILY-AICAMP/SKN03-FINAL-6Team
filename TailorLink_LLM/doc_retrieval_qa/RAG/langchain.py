from RAG.llm import get_OpenAI
from RAG.prompt import get_prompt


def get_langchain():
    prompt = get_prompt()
    llm = get_OpenAI()
