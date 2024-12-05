
from langchain_core.prompts import PromptTemplate
# 단계 6: 프롬프트 생성(Create Prompt)
# 프롬프트를 생성합니다.
def get_prompt():
    prompt = PromptTemplate.from_template(
        """You are an assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Answer in Korean.

    #Context: 
    {context}

    #Question:
    {question}

    #Answer:"""
    )
    return prompt