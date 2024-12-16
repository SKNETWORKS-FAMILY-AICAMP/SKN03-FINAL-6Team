import requests
import urllib.parse  # URL 디코딩을 위한 모듈
import json


def get_brand_list(headers):
    url = "https://api.codef.io/v1/kr/car/brand-list"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            # URL 디코딩
            decoded_response = urllib.parse.unquote(response.text)
            print("디코딩 된 응답:", decoded_response)
            
            # JSON 변환
            json_response = json.loads(decoded_response)
            return json_response
        except json.JSONDecodeError:
            print("디코딩 후 JSON 변환 실패.")
            return None
    else:
        print("제조사 목록 조회 실패:", response.status_code, response.text)
        return None
    
    
    
def get_model_list(headers, brand_code):
    
    brand_code_encode = urllib.parse.quote(brand_code)
    
    url = f"https://api.codef.io/v1/kr/car/model-list?brand={brand_code_encode}"
    response = requests.get(url=url, headers=headers)
    
    if response.status_code == 200:
        try:
            # URL 디코딩
            decoded_response = urllib.parse.unquote(response.text)
            print("디코딩 된 응답:", decoded_response)
            
            # JSON 변환
            json_response = json.loads(decoded_response)
            return json_response
        except json.JSONDecodeError:
            print("디코딩 후 JSON 변환 실패.")
            return None
    else:
        print("차량 모델 목록 조회 실패:", response.status_code, response.text)
        return None
    
    
    
def get_year_list(headers, brand_code, model_code, start_date):
    
    brand_code_encode = urllib.parse.quote(brand_code)
    brand_code_encode = urllib.parse.quote(model_code)
    
    
    url = f"https://api.codef.io/v1/kr/car/year-list?brand={brand_code_encode}&model={brand_code_encode}&startDate={start_date}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            # URL 디코딩
            decoded_response = urllib.parse.unquote(response.text)
            print("디코딩 된 응답:", decoded_response)
            
            # JSON 변환
            json_response = json.loads(decoded_response)
            return json_response
        except json.JSONDecodeError:
            print("디코딩 후 JSON 변환 실패.")
            return None
    else:
        print("등록 연도 목록 조회 실패:", response.status_code, response.text)
        return None
    
    
    
def get_detail_list(headers, brand_code, model_code, year_code):
    
    brand_code_encode = urllib.parse.quote(brand_code)
    model_code_encode = urllib.parse.quote(model_code)
    
    url = f"https://api.codef.io/v1/kr/car/detail-list?brand={brand_code_encode}&model={model_code_encode}&year={year_code}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            # URL 디코딩
            decoded_response = urllib.parse.unquote(response.text)
            print("디코딩 된 응답:", decoded_response)
            
            # JSON 변환
            json_response = json.loads(decoded_response)
            return json_response
        except json.JSONDecodeError:
            print("디코딩 후 JSON 변환 실패.")
            return None
    else:
        print("상세 차량명 목록 조회 실패:", response.status_code, response.text)
        return None
    
    
    
def get_option_list(headers, brand_code, model_code, year_code, detail_code):
    
    brand_code_encode = urllib.parse.quote(brand_code)
    model_code_encode = urllib.parse.quote(model_code)
    year_code_encode = urllib.parse.quote(year_code)
    detail_code_encode = urllib.parse.quote(detail_code)
    
    url = f"https://api.codef.io/v1/kr/car/option-list?brand={brand_code_encode}&model={model_code_encode}&year={year_code_encode}&option={detail_code_encode}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        try:
            # URL 디코딩
            decoded_response = urllib.parse.unquote(response.text)
            print("디코딩 된 응답:", decoded_response)
            
            # JSON 변환
            json_response = json.loads(decoded_response)
            return json_response
        except json.JSONDecodeError:
            print("디코딩 후 JSON 변환 실패.")
            return None
    else:
        print("옵션명 목록 조회 실패:", response.status_code, response.text)
        return None