import requests
import urllib.parse
import json
from langchain.tools import tool
from pydantic import BaseModel
import os
from dotenv import load_dotenv


# 임시 코드
from typing_extensions import Annotated, Sequence, TypedDict
from langchain.schema import BaseMessage

# 헤더 모델 정의
class Headers(BaseModel):
    Authorization: str
    Content_Type: str
    
class Vehicle(BaseModel):
    brand: str = ""  # 기본값 설정
    model: str = ""
    date: int = 0
    year: str = ""
    detail: str = ""
    option: str = ""

class State(BaseModel):
    headers : Headers
    vehicle: Vehicle
    messages: Annotated[Sequence[BaseMessage], "add_messages"]
    ask_human: bool


class HumanRequest(BaseModel):
    """Forward the conversation to an expert. Use when you can't assist directly or the user needs assistance that exceeds your authority.
    To use this function, pass the user's 'request' so that an expert can provide appropriate guidance.
    """

    request: str

# 1. 제조사 목록 조회 함수
@tool("get_brand_list", return_direct=True)
def get_brand_list_tool(State: dict) -> dict:
    """
    자동차 제조사 목록을 조회하는 함수입니다.

    Args:
        headers (dict): API 호출 시 필요한 헤더 정보.

    Returns:
        dict: 제조사 목록 JSON 데이터.
    """
    print("--제조사 목록을 불러옵니다.")
    headers = State.headers # headers 추출
    url = "https://api.codef.io/v1/kr/car/brand-list"
    response = requests.get(url=url, headers=headers)
    
    if response.status_code == 200:
        try:
            decoded_response = urllib.parse.unquote(response.text)
            return json.loads(decoded_response)
        except json.JSONDecodeError:
            return {"error": "JSON 변환 실패"}
    else:
        return {"error": f"API 요청 실패: {response.status_code}"}


# 2. 모델 목록 조회 함수
@tool("get_model_list", return_direct=True)
def get_model_list_tool(State: dict) -> dict:
    """
    자동차 모델 목록을 조회하는 함수입니다.

    Args:
        headers (dict): API 호출 시 필요한 헤더 정보.
        brand_code (str): 브랜드 코드.

    Returns:
        dict: 모델 목록 JSON 데이터.
    """
    print("--모델 목록을 불러옵니다.")
    headers = State.headers
    brand_code = State.brand_code
    
    brand_code_encode = urllib.parse.quote(brand_code)
    url = f"https://api.codef.io/v1/kr/car/model-list?brand={brand_code_encode}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            decoded_response = urllib.parse.unquote(response.text)
            return json.loads(decoded_response)
        except json.JSONDecodeError:
            return {"error": "JSON 변환 실패"}
    else:
        return {"error": f"API 요청 실패: {response.status_code}"}


# 3. 연식 목록 조회 함수
@tool("get_year_list", return_direct=True)
def get_year_list_tool(State: dict) -> dict:
    """
    차량 연식 목록을 조회하는 함수입니다.

    Args:
        headers (dict): API 호출 시 필요한 헤더 정보.
        brand_code (str): 브랜드 코드.
        model_code (str): 모델 코드.
        start_date (str): 시작 날짜.

    Returns:
        dict: 연식 목록 JSON 데이터.
    """
    print("--연식 목록을 불러옵니다.")
    headers = State.headers
    brand_code = State.brand_code
    start_date = State.start_date
    
    brand_code_encode = urllib.parse.quote(brand_code)
    model_code_encode = urllib.parse.quote(model_code)

    url = f"https://api.codef.io/v1/kr/car/year-list?brand={brand_code_encode}&model={model_code_encode}&startDate={start_date}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            decoded_response = urllib.parse.unquote(response.text)
            return json.loads(decoded_response)
        except json.JSONDecodeError:
            return {"error": "JSON 변환 실패"}
    else:
        return {"error": f"API 요청 실패: {response.status_code}"}


# 4. 상세 차량명 목록 조회 함수
@tool("get_detail_list", return_direct=True)
def get_detail_list_tool(State: dict) -> dict:
    """
    차량 상세 목록을 조회하는 함수입니다.

    Args:
        headers (dict): API 호출 시 필요한 헤더 정보.
        brand_code (str): 브랜드 코드.
        model_code (str): 모델 코드.
        year_code (str): 연식 코드.

    Returns:
        dict: 상세 차량명 목록 JSON 데이터.
    """
    print("--세부 모델 목록을 불러옵니다.")
    headers = State.headers
    brand_code = State.brand_code
    model_code = State.model_code
    year_code = State.year_code

    
    brand_code_encode = urllib.parse.quote(brand_code)
    model_code_encode = urllib.parse.quote(model_code)

    url = f"https://api.codef.io/v1/kr/car/detail-list?brand={brand_code_encode}&model={model_code_encode}&year={year_code}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            decoded_response = urllib.parse.unquote(response.text)
            return json.loads(decoded_response)
        except json.JSONDecodeError:
            return {"error": "JSON 변환 실패"}
    else:
        return {"error": f"API 요청 실패: {response.status_code}"}


# 5. 옵션 목록 조회 함수
@tool("get_option_list", return_direct=True)
def get_option_list_tool(State: dict) -> dict:
    """
    차량 옵션 목록을 조회하는 함수입니다.

    Args:
        headers (dict): API 호출 시 필요한 헤더 정보.
        brand_code (str): 브랜드 코드.
        model_code (str): 모델 코드.
        year_code (str): 연식 코드.
        detail_code (str): 상세 옵션 코드.

    Returns:
        dict: 옵션 목록 JSON 데이터.
    """
    print("--세부 옵션 목록을 불러옵니다.")
    headers = State.headers
    brand_code = State.brand_code
    model_code = State.model_code
    year_code = State.year_code
    detail_code = State.detail_code
    
    
    brand_code_encode = urllib.parse.quote(brand_code)
    model_code_encode = urllib.parse.quote(model_code)
    year_code_encode = urllib.parse.quote(year_code)
    detail_code_encode = urllib.parse.quote(detail_code)

    url = f"https://api.codef.io/v1/kr/car/option-list?brand={brand_code_encode}&model={model_code_encode}&year={year_code_encode}&option={detail_code_encode}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            decoded_response = urllib.parse.unquote(response.text)
            return json.loads(decoded_response)
        except json.JSONDecodeError:
            return {"error": "JSON 변환 실패"}
    else:
        return {"error": f"API 요청 실패: {response.status_code}"}
