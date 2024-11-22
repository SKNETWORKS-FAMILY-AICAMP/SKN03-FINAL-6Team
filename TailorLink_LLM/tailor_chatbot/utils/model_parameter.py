# 모델 파라미터 설정
def langchain_param():
    params = {
        "temperature": 0.9,         # 생성된 텍스트의 다양성 조정
        "max_tokens": 2056,          # 생성할 최대 토큰 수
        "frequency_penalty": 0.5,   # 이미 등장한 단어의 재등장 확률
        "presence_penalty": 0.5,    # 새로운 단어의 도입을 장려
    }
    return params  