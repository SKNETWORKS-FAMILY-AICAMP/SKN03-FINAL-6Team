from langchain.chat_models import ChatOpenAI
from langchain_ollama import ChatOllama

# 공통 LLM 설정
DEFAULT_TEMPERATURE = 0.0


# OpenAI 모델 생성 함수
def create_openai_model(model_name="gpt-4o-mini", temperature=DEFAULT_TEMPERATURE):
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
    return ChatOpenAI(model_name=model_name, temperature=temperature)


# Ollama 모델 생성 함수
def create_ollama_model(model_id: str, temperature=DEFAULT_TEMPERATURE):
    """
    Ollama 모델 객체를 생성합니다.

    Parameters:
        model_id (str): 사용할 Ollama 모델 ID.
        temperature (float): 출력의 다양성을 조정하는 매개변수. 기본값은 0.0.

    Returns:
        ChatOllama: 설정된 Ollama LLM 인스턴스.
    """
    if not isinstance(model_id, str):
        raise ValueError("model_id must be a string.")
    return ChatOllama(model=model_id, temperature=temperature)
