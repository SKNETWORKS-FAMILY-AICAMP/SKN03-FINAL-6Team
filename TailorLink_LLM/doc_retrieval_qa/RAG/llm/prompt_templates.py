
from langchain_core.prompts import PromptTemplate
# 단계 6: 프롬프트 생성(Create Prompt)

# 프롬프트를 생성합니다.
def get_genesis_manual_classification_prompt():
    prompt = PromptTemplate.from_template(
        """
        You are an expert in Genesis Q&A.  
        Determine whether the user's question is related to 'Genesis' or general vehicle usage and maintenance.  
        
        Criteria:  
        - If the question mentions 'Genesis' vehicles or models (e.g., G70, G80, G90) and asks about usage, maintenance, functionality, update methods, or other manual-related inquiries, answer "yes."  
        - If the question does not explicitly mention 'Genesis' but refers to general vehicle usage, maintenance, or functionality that could apply to any vehicle, including 'Genesis,' answer "yes."  
        - If the question is unrelated to vehicles or does not fit the above criteria, answer "no."  
        
        Assume that general vehicle-related questions (e.g., how to start a car, how to check oil) are indirectly relevant to 'Genesis' unless explicitly stated otherwise.  
        
        Your answer must be in English, and it should be either "yes" or "no."  
        
        #Question:  
        {question}  
        
        #Answer:
        """
    )
    return prompt

def get_answer_with_context_prompt():
    prompt = PromptTemplate.from_template(
        """
        너는 전문적인 사용자 도우미이며, 주어진 Context를 기반으로 사용자의 질문에 대한 정확하고 상세한 답변을 작성해야 한다.  
        답변은 한글로 작성하며, 마크다운 형식을 사용해 가독성을 높여야 한다.  
        답변에는 항상 정보의 출처를 명시하며, 기존 학습된 데이터를 사용하지 않고 Context를 통해 제공된 정보 만을 가지고 답변해야 한다.  
        필요한 경우, 추가적인 예시나 세부 정보를 포함해 사용자의 질문에 완벽하게 답변하라.  
        
        # Context:  
        {context}
        
        # Question:  
        {question}  
        
        # Answer:  
        ### 질문에 대한 답변:  
        질문에 대한 구체적인 답변 작성
        
        ### 출처:  
        1. CONTEXT 기반 정보: CONTEXT에서 관련된 정보 요약  

        """
    )
    return prompt

def get_score_answer_prompt():
    prompt = PromptTemplate.from_template(
        """
        너는 전문적인 사용자 도우미이며, 주어진 Question과 Answer를 가지고 Answer가 사용자가 원하는 답인지 점수를 계산해야 한다.  
        점수를 계산할 때, Answer가 주어진 Context외의 정보를 가지고 있으면 안된다.
        JSON 형식 Reason과 Score로 대답해라.
        # Context:  
        {context}
        
        # Question:  
        {question}  
        
        # Answer:  
        {answer}
        
        {{
          "reason": "value1",
          "score": 100
        }}     
        """
    )
    return prompt

def get_rewrite_query_prompt():
    prompt = PromptTemplate.from_template(
        """
        Rewrite the query '{question}' to improve retrieval quality. Use the context of previous questions and generate only one improved query. Ensure the new query does not overlap with any of the previous questions.

        # Previous questions: 
        {previous}

        """
    )
    return prompt