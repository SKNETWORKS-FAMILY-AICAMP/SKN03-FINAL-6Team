from langchain_openai import ChatOpenAI

def langchain_param():
    params = {
        "temperature": 0.7,         # 생성된 텍스트의 다양성 조정
        "max_tokens": 1000,          # 생성할 최대 토큰 수
        "frequency_penalty": 0.5,   # 이미 등장한 단어의 재등장 확률
        "presence_penalty": 0.5,    # 새로운 단어의 도입을 장려
    }
    return params


def get_client(model_id: str = "gpt-4o-mini"):
    try:
        return ChatOpenAI(model=model_id, **langchain_param())
    except Exception as e:
        return (f"ChatOpenAI를 불러오지 못했습니다.: {e}")
