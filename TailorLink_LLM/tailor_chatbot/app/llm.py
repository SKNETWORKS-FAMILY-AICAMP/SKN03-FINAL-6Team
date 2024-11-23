# app/llm.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# KoGPT2 모델 로드
model_name = "skt/kogpt2-base-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(model_name)

# LLM을 활용한 사용자 입력 분석 함수
def analyze_user_input(user_input: str) -> dict[str, str]:
    prompt = f"사용자의 입력에서 예산 상태(저예산, 중예산, 고예산)와 선호하는 차종(소형차, 중형차, SUV 등)을 추출하세요.\n\n사용자 입력: \"{user_input}\"\n\n예산 상태:"
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=100, do_sample=True, top_p=0.95, num_return_sequences=1)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # 간단한 문자열 처리를 통해 정보 추출
    economic_status = "mid"
    if "저예산" in generated_text or "저렴" in generated_text:
        economic_status = "low"
    elif "중예산" in generated_text:
        economic_status = "mid"
    elif "고예산" in generated_text or "고급" in generated_text:
        economic_status = "high"
    
    car_type = None
    if "소형차" in generated_text:
        car_type = "소형차"
    elif "중형차" in generated_text:
        car_type = "중형차"
    elif "SUV" in generated_text:
        car_type = "SUV"
    
    return {"economic_status": economic_status, "car_type": car_type}
