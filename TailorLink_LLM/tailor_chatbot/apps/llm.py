from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
import re 


# 환경 변수 로드
load_dotenv()


def langchain_param():
    params = {
        "temperature": 0.9,  # 더 자연스러운 응답 생성
        "max_tokens": 500,  # 응답 크기 제한
        "frequency_penalty": 0.2,
        "presence_penalty": 0.6
    }
    return params

def get_client(model_id: str = "gpt-4"):
    return ChatOpenAI(
        model_name=model_id,
        **langchain_param()
    )

def is_simple_request(user_input: str) -> bool:
    simple_keywords = ["소형차", "SUV", "고급차", "연비", "가격", "추천"]
    return any(keyword in user_input for keyword in simple_keywords) and len(user_input.split()) <= 10

def analyze_user_request(user_input: str) -> str:
    chat = get_client()
    messages = [
        {"role": "system", "content": "당신은 자동차 구매를 도와주는 친절한 어시스턴트입니다."},
        {"role": "user", "content": f"{user_input}"}
    ]
    response = chat.invoke(messages)
    return response.content

def extract_budget_from_input(user_input: str) -> int:
    # 입력 문자열에서 모든 숫자 찾기
    numbers = re.findall(r'\d+', user_input)
    if numbers:
        return int(numbers[0])
    else:
        return 2000

def extract_features_from_input(user_input: str) -> dict:
    age = 30  # 기본값
    if "20대" in user_input:
        age = 20
    elif "30대" in user_input:
        age = 30

    # 예산 추출
    budget = extract_budget_from_input(user_input)

    return {"age": age, "budget": budget}

def recommend_cars(user_input: str) -> str:
    # if is_simple_request(user_input):
    #     print("간단한 요청입니다. DeepFM을 사용합니다.")
    #     user_features = extract_features_from_input(user_input)
    #     recommendations = recommend_with_deepfm(user_features, get_sample_car_data(), deepfm_model)
    #     return format_deepfm_response(recommendations)
    # else:
    #     print("복잡한 요청입니다. LangChain을 사용합니다.")
    return analyze_user_request(user_input)

def format_deepfm_response(recommendations: list) -> str:
    if not recommendations:
        return "추천할 차량이 없습니다. 조건을 변경해 주세요."

    response = "제가 추천하는 차량은 다음과 같습니다:\n"
    for i, (car, score) in enumerate(recommendations, start=1):
        response += f"{i}. {car['make']} {car['model']} - {car['type']} (추천 점수: {score:.2f})\n"
    response += "더 궁금한 점이 있으면 말씀해주세요!"
    return response

