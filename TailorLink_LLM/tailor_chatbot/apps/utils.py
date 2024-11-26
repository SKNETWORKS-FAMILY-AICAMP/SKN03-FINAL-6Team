# app/utils.py
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def langchain_param():
        params = {
            "temperature": 0.9,  # 더 자연스러운 응답 생성
            "max_tokens": 500,  # 응답 크기 제한
            "frequency_penalty": 0.2,
            "presence_penalty": 0.6
        }
        return params

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

def get_openai_response(user_input: str) -> str:
    client = OpenAIClientSingleton.get_instance()
    messages = [
        {"role": "system", "content": "당신은 자동차 추천을 도와주는 친절한 어시스턴트입니다."},
        {"role": "user", "content": user_input}
    ]
    response = client.invoke(messages)
    return response.content
