import os
import torch
from dotenv import load_dotenv
from cachetools import TTLCache, cached
from cachetools.keys import hashkey
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
# from langchain_community.llms import HuggingFacePipeline
# from huggingface_hub import login
from .cilent import get_client
load_dotenv()

# token = os.getenv("HUGGINGFACE_KEY")
# if not token:
#     raise ValueError("HUGGINGFACE_KEY 환경 변수가 설정되지 않았습니다.")

# login(token=token)
# os.environ["HF_HOME"] = "./cache/"

# # LLM 모델 설정 (HuggingFace 파이프라인)
# model_name = "meta-llama/Llama-2-7b-hf" 
# tokenizer = AutoTokenizer.from_pretrained(
#     model_name,
#     use_auth_token=token,
#     trust_remote_code=True
# )   
# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     device_map="auto",
#     torch_dtype=torch.float16,
#     use_auth_token=token,
#     trust_remote_code=True
# )

# pipe = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     max_length=4096,
#     temperature=0.7,
#     top_p=0.9,
#     repetition_penalty=1.2,
#     truncation=True
# )

# llm = HuggingFacePipeline(pipeline=pipe)

# 캐시 설정
openai_cache = TTLCache(maxsize=100, ttl=600)

def get_toolkit():
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT", 3306)
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    
    if not all([db_host, db_port, db_user, db_password, db_name]):
        raise ValueError("데이터베이스 환경 변수를 설정해주세요.")
    
    db_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    db = SQLDatabase.from_uri(db_uri)
    
    toolkit = SQLDatabaseToolkit(db=db, llm=get_client())  # LLM과 SQLDatabase 연결
    return toolkit
    
    

