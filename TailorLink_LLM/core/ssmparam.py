import boto3
import os

def get_ssm_parameter(parameter_name, with_decryption=True):
    """
    SSM Parameter Store에서 지정된 매개변수 값을 가져옵니다.

    Args:
        parameter_name (str): SSM Parameter Store에서 가져올 매개변수 이름
        with_decryption (bool): 암호화된 값을 복호화할지 여부 (기본값: True)

    Returns:
        str: 매개변수 값

    Raises:
        botocore.exceptions.ClientError: 매개변수를 가져오는 데 실패한 경우 예외 발생
    """
    # SSM 클라이언트 생성
    ssm = boto3.client('ssm')

    try:
        # 매개변수 가져오기
        response = ssm.get_parameter(
            Name=parameter_name,
            WithDecryption=with_decryption
        )
        # 매개변수 값 반환
        return response['Parameter']['Value']
    except Exception as e:
        print(f"Failed to retrieve parameter {parameter_name}: {e}")
        return None

from boto3.session import Session
from typing import List, Optional

def loadenv():
    """
    AWS Parameter Store에서 환경 변수를 로드하고 os.environ에 추가합니다.
    """
    # SSM 클라이언트 생성
    ssm = boto3.client('ssm')

    parameter_names = [
        '/tailorlink/milvus/MILVUS_TOKEN',
        '/tailorlink/milvus/MILVUS_URI',
        '/tailorlink/mysql/MYSQL_DB_NAME',
        '/tailorlink/mysql/MYSQL_USER',
        '/tailorlink/mysql/MYSQL_PASSWORD',
        '/tailorlink/mysql/MYSQL_URI',
        '/tailorlink/openai/OPENAI_API_KEY'
    ]

    for parameter_name in parameter_names:
        try:
            # Parameter Store에서 값 가져오기
            value = get_ssm_parameter(parameter_name)

            # 환경 변수로 설정
            key_name = parameter_name.split("/")[-1]  # 마지막 부분을 환경 변수 이름으로 사용
            os.environ[key_name] = value
            print(f"Environment variable set: {key_name}")

        except Exception as e:
            print(f"Failed to load parameter: {parameter_name}, Error: {e}")