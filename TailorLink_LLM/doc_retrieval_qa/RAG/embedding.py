from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
import os
import warnings

# 경고 무시
warnings.filterwarnings("ignore")
# ./cache/ 경로에 다운로드 받도록 설정
os.environ["HF_HOME"] = "./cache/"

def get_openai_embedding():
    # 단계 3: 임베딩(Embedding) 생성
    embeddings = OpenAIEmbeddings()
    return embeddings

def get_huggingface_embedding(model_name="intfloat/multilingual-e5-large-instruct",
                              device='cpu'):
    # model_name = "BAAI/bge-m3"
    # model_name = "intfloat/multilingual-e5-large-instruct"
    model_name = model_name
    model_kwargs = {"device": device}
    encode_kwargs = {"normalize_embeddings": True}
    hf_embeddings = HuggingFaceEmbeddings(
        model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
    )
    return hf_embeddings