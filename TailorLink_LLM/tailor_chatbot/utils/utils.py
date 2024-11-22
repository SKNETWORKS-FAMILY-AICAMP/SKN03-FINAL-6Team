import os
import boto3

# 환경 변수에서 OpenAI API 키 설정
def __set_openai_api_key():
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None)

    if not OPENAI_API_KEY:
        # AWS SSM에서 OpenAI API 키를 가져오기
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name='/CICD/FASTAPI/OPENAI_API_KEY', WithDecryption=True)
        os.environ['OPENAI_API_KEY'] = parameter['Parameter']['Value']


# 초기화 함수
def init_chatbot(session_state):
    """
    FastAPI 환경에서 상태 초기화를 처리하는 함수.
    session_state는 사용자별 메시지 상태를 저장하는 딕셔너리 형태로 사용.
    """
    __set_openai_api_key()

    if "messages" not in session_state:
        session_state["messages"] = []
