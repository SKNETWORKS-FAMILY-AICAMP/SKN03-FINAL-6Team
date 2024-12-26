import boto3
from app.core.logger import logger

def get_ssm_parameter(parameter_name: str, with_decryption: bool = True) -> str:
    """
    SSM Parameter Store에서 매개변수 값을 가져옵니다.

    Args:
        parameter_name (str): SSM Parameter Store의 매개변수 이름
        with_decryption (bool): 암호화된 값 복호화 여부 (기본값: True)

    Returns:
        str: 매개변수 값

    Raises:
        Exception: 값을 가져오지 못했을 때 예외 발생
    """
    ssm = boto3.client('ssm')
    try:
        response = ssm.get_parameter(Name=parameter_name, WithDecryption=with_decryption)
        value = response['Parameter']['Value']
        logger.info(f"Retrieved parameter: {parameter_name}")
        return value
    except Exception as e:
        logger.error(f"Failed to retrieve parameter {parameter_name}: {e}")
        return ''
        # raise Exception(f"Failed to retrieve parameter {parameter_name}") from e
