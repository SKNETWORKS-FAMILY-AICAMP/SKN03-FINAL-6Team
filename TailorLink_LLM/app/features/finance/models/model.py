from langchain_openai import ChatOpenAI

# 공통 LLM 설정
DEFAULT_TEMPERATURE = 0.0

# OpenAI 모델 생성 함수
def get_OpenAI(model_name="gpt-4o-mini", temperature=DEFAULT_TEMPERATURE):
    """
    OpenAI 모델 객체를 생성합니다.

    Parameters:
        model_name (str): 사용할 모델 이름. 기본값은 'gpt-4o-mini'.
        temperature (float): 출력의 다양성을 조정하는 매개변수. 기본값은 0.0.

    Returns:
        ChatOpenAI: 설정된 OpenAI LLM 인스턴스.
    """
    if not isinstance(model_name, str):
        raise ValueError("model_name must be a string.")
    return get_OpenAI(model_name=model_name, temperature=temperature)