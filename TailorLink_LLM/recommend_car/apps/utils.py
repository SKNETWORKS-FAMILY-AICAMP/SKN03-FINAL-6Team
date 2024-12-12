import os
import logging
import sqlite3

import requests
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase

load_dotenv()

logging.basicConfig(
    level=logging.DEBUG,  
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chatbot.log"),  
    ],
)
logger = logging.getLogger("recommend_car")

def connect_aws_db():
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", 3306)
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    
    if not all([db_host, db_port, db_user, db_password, db_name]):
        raise ValueError("데이터베이스 환경 변수를 설정해주세요.")
    
    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    db = SQLDatabase.from_uri(db_uri)

    return db

    
    

