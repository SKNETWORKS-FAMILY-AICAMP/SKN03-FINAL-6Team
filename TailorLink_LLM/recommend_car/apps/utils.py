import os
from dotenv import load_dotenv
from typing import List, Dict
from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from langchain_openai import ChatOpenAI

load_dotenv()

# OpenAI 캐싱
openai_cache = TTLCache(maxsize=100, ttl=600)

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

def langchain_param():
    return {
        "temperature": 0.9,
        "max_tokens": 500,
        "frequency_penalty": 0.2,
        "presence_penalty": 0.6,
    }


class OpenAIClientSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ChatOpenAI(
                model_name="gpt-4",
                **langchain_param()
            )
        return cls._instance

@cached(openai_cache , key=lambda messages: hashkey(tuple((msg['role'], msg['content']) for msg in messages)))
def get_openai_response(messages: List[Dict[str, str]]) -> str:
    client = OpenAIClientSingleton.get_instance()
    response = client.invoke(messages)
    return response.content

