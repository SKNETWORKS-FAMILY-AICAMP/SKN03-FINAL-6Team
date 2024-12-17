import boto3

def get_ssm_parameter(parameter_name, with_decryption=True):
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