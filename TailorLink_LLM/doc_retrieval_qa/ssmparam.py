import boto3


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