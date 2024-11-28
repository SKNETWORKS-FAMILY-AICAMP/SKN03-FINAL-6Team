import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import List, Dict

# 환경 변수 로드
load_dotenv()

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

def get_openai_response(messages: List[Dict[str, str]]) -> str:
    client = OpenAIClientSingleton.get_instance()

    # OpenAI 호출 및 응답 생성
    response = client.invoke(messages)
    return response.content
