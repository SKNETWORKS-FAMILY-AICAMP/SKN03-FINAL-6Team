# base image
FROM python:3.12-slim

# os 업데이트 & 설치 
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    awscli \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 코드 복사 
COPY . /app
# 실행 폴더 정의 
WORKDIR /app

# 필요한 라이브러리 설치
RUN pip3 install --no-cache-dir --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt
#RUN pip3 install --no-cache-dir uvicorn

ENV PYTHONPATH=/app

# 실행 포트 정의 
EXPOSE 8000
# 컨테이너 실행 유무 확인 
HEALTHCHECK CMD curl --fail http://localhost:8000/health || exit 1

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

