import logging
from logging.handlers import RotatingFileHandler

# 로깅 포맷 정의
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 로깅 설정 함수
def setup_logger(name: str = "fastapi_project", level: int = logging.INFO) -> logging.Logger:
    """
    로거를 설정하고 반환합니다.

    Args:
        name (str): 로거 이름
        level (int): 로깅 레벨 (기본값: INFO)

    Returns:
        logging.Logger: 설정된 로거 객체
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 콘솔 핸들러 추가
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console_handler)

    # 파일 핸들러 추가 (RotatingFileHandler)
    file_handler = RotatingFileHandler(
        "tailorlink.log",        # 로그 파일 이름
        maxBytes=10_000,  # 최대 파일 크기 (10KB)
        backupCount=1     # 백업 파일 개수 (최대 5개)
    )
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(file_handler)

    return logger


# 로거 생성
logger = setup_logger()
