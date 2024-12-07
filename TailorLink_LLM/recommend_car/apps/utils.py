#import os
#from dotenv import load_dotenv
#from typing import List, Dict
#from cachetools import TTLCache, cached
#from cachetools.keys import hashkey
#from langchain_openai import ChatOpenAI

#load_dotenv()

# OpenAI 캐싱
#openai_cache = TTLCache(maxsize=100, ttl=600)

#openai_api_key = os.getenv("OPENAI_API_KEY")
#if not openai_api_key:
#    raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")

#def langchain_param():
#    return {
#        "temperature": 0.9,
#        "max_tokens": 500,
#        "frequency_penalty": 0.2,
#        "presence_penalty": 0.6,
#    }


#class OpenAIClientSingleton:
#    _instance = None

#    @classmethod
#    def get_instance(cls):
#        if cls._instance is None:
#            cls._instance = ChatOpenAI(
#                model_name="gpt-4",
#                **langchain_param()
#            )
#        return cls._instance

#@cached(openai_cache , key=lambda messages: hashkey(tuple((msg['role'], msg['content']) for msg in messages)))
#def get_openai_response(messages: List[Dict[str, str]]) -> str:
#    client = OpenAIClientSingleton.get_instance()
#    response = client.invoke(messages)
#    return response.content

import os
from dotenv import load_dotenv
from typing import List, Dict
from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms import HuggingFacePipeline
from huggingface_hub import login
import torch

load_dotenv()

token = os.getenv("HUGGINGFACE_KEY")
if not token:
    raise ValueError("HUGGINGFACE_KEY 환경 변수가 설정되지 않았습니다.")

login(token=token)

#임베딩 모델
embedding_model_name = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(embedding_model_name)

def embedding_function(texts: List[str]):
    return embedder.encode(texts)

# LLM 모델 설정
model_name = "meta-llama/Llama-2-7b-hf" 
tokenizer = AutoTokenizer.from_pretrained(
    model_name,
    use_auth_token=token,
    trust_remote_code=True,
    local_files_only=True
)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16,
    use_auth_token=token,
    trust_remote_code=True,
    local_files_only=True
)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_length=1024,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.2
)

llm = HuggingFacePipeline(pipeline=pipe)

# 캐시 설정
openai_cache = TTLCache(maxsize=100, ttl=600)

@cached(openai_cache, key=lambda messages: hashkey(tuple((msg['role'], msg['content']) for msg in messages)))
def get_llm_response(messages: List[Dict[str, str]]) -> str:
    # role-based messages → prompt로 변환
    system_prompts = [m['content'] for m in messages if m['role'] == 'system']
    user_prompts = [m['content'] for m in messages if m['role'] == 'user']
    assistant_context = [m['content'] for m in messages if m['role'] == 'assistant']

    system_prompt = "\n".join(system_prompts)
    assistant_history = "\n".join([f"Assistant: {a}" for a in assistant_context])
    user_prompt = "\n".join([f"User: {u}" for u in user_prompts])

    final_prompt = f"{system_prompt}\n{assistant_history}\n{user_prompt}\nAssistant:"
    response = llm(final_prompt)
    return response.strip()