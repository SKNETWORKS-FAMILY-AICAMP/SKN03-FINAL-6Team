from pydantic_settings import BaseSettings
from pydantic import Field
from app.core.ssmparam import get_ssm_parameter
import os

class Settings(BaseSettings):
    """
    애플리케이션 설정 클래스.
    AWS SSM Parameter Store에서 값을 가져와 설정.
    """
    # 프로젝트 기본 설정
    PROJECT_NAME: str = Field(default="TailorLink", description="프로젝트 이름")
    PROJECT_DESCRIPTION: str =  Field(default="OpenAI를 사용한 채팅 봇", description="프로젝트 설명")
    PROJECT_VERSION: str =  Field(default="1.0.6", description="프로젝트 버전")
    DEBUG: bool = Field(default=False, description="디버그 모드 활성화 여부")
    # 데이터베이스 설정
    DATABASE_URL: str = Field(
        default_factory=lambda: get_ssm_parameter('/tailorlink/mysql/MYSQL_URI'),
        description="데이터베이스 연결 URL"
    )
    DATABASE_USER: str = Field(
        default_factory=lambda: get_ssm_parameter('/tailorlink/mysql/MYSQL_USER'),
        description="데이터베이스 사용자 이름"
    )
    DATABASE_PASSWORD: str = Field(
        default_factory=lambda: get_ssm_parameter('/tailorlink/mysql/MYSQL_PASSWORD'),
        description="데이터베이스 비밀번호"
    )
    DATABASE_NAME: str = Field(
        default_factory=lambda: get_ssm_parameter('/tailorlink/mysql/MYSQL_DB_NAME'),
        description="데이터베이스 이름"
    )

    # OpenAI API 설정
    OPENAI_API_KEY: str = Field(
        default_factory=lambda: get_ssm_parameter('/tailorlink/openai/OPENAI_API_KEY'),
        description="OpenAI API 키"
    )

    # Milvus 설정
    MILVUS_URI: str = Field(
        default_factory=lambda: get_ssm_parameter('/tailorlink/milvus/MILVUS_URI'),
        description="Milvus URI"
    )
    MILVUS_TOKEN: str = Field(
        default_factory=lambda: get_ssm_parameter('/tailorlink/milvus/MILVUS_TOKEN'),
        description="Milvus 인증 토큰"
    )
    MILVUS_ALIAS: str = Field(default='tailorlink', description='Milvus alias')

    MILVUS_DB_NAME: str = Field(default='tailorlink', description='Milvus database name')

    LANGCHAIN_API_KEY: str = Field(
        default_factory=lambda: get_ssm_parameter('/tailorlink/langchain/LANGCHAIN_API_KEY'),
        description="Langchain API 키"
    )

    LANGCHAIN_ENDPOINT: str = Field(
        default_factory=lambda: get_ssm_parameter('/tailorlink/langchain/LANGCHAIN_ENDPOINT'),
        description="Langchain endpoint"
    )

    MILVUS_CHECK_INTERVAL: int = Field(
        default=30,
    )
    SQLALCHEMY_CHECK_INTERVAL: int = Field(
        default=30,
    )

    # 클래스 초기화 시 os.environ에 값 추가
    def __init__(self, **data):
        super().__init__(**data)
        # OPENAI_API_KEY를 os.environ에 추가
        if 'OPENAI_API_KEY' not in os.environ:
            os.environ['OPENAI_API_KEY'] = self.OPENAI_API_KEY
        if 'LANGCHAIN_API_KEY' not in os.environ:
            os.environ['LANGCHAIN_API_KEY'] = self.LANGCHAIN_API_KEY
        if 'LANGCHAIN_TRACING_V2' not in os.environ:
            os.environ['LANGCHAIN_TRACING_V2'] = "true"
        if 'LANGCHAIN_PROJECT' not in os.environ:
            os.environ['LANGCHAIN_PROJECT'] = 'TailorLink'


# 설정 객체 생성
settings = Settings()
