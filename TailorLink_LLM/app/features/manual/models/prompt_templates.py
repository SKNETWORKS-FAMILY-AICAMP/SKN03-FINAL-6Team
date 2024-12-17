
from langchain_core.prompts import PromptTemplate
# 단계 6: 프롬프트 생성(Create Prompt)

# 프롬프트를 생성합니다.
def create_genesis_classification_prompt():
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

def create_context_based_answer_prompt():
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

def create_answer_evaluation_prompt():
    prompt = PromptTemplate.from_template(
        """
        너는 전문적인 사용자 도우미이며, 주어진 Question과 Answer를 가지고 Answer가 사용자가 원하는 답인지 점수를 계산해야 한다.  
        점수를 계산할 때, Answer가 주어진 Context 외의 정보를 가지고 있으면 안된다.
        최고 점수를 100을 기준으로 점수를 계산해라.
        JSON 형식 Reason과 Score로 대답해라.
        # Context:  
        {context}
        
        # Question:  
        {question}  
        
        # Answer:  
        {answer}
        
        {{
          "reason": "value",
          "score": 점수
        }}     
        """
    )
    return prompt

def create_query_rewrite_prompt():
    prompt = PromptTemplate.from_template(
        """
        Rewrite the query '{question}' to improve retrieval quality. Use the context of previous questions and generate only one improved query. Ensure the new query does not overlap with any of the previous questions.

        # Previous questions: 
        {previous}

        """
    )
    return prompt

def create_question_split_prompt():
    prompt = PromptTemplate.from_template(
        """
        너는 RAG 전문가이다.  
        주어진 질문이 복합적인 내용으로 구성된 경우, 각 질문을 독립적인 단위로 분리해야 한다.  
        질문을 분리할 때, 각 질문이 명확하고 RAG의 검색 및 답변 생성 품질이 최대화되도록 작성해야 한다.  

        ### 지침:
        - 질문 분리는 논리적 흐름에 따라 자연스럽게 이루어져야 한다.
        - 각 질문은 특정 주제나 개념에 집중하여 검색 가능한 형태로 작성해야 한다.
        - 분리된 결과는 **리스트 형식**으로 반환하며, 추가 설명 없이 리스트만 출력해야 한다.

        ### 예시:  
        입력: "g90 시동 거는 방법과 스펙을 알려줘."  
        출력: ["g90의 시동 거는 방법은 무엇인가?", "g90의 스펙은 무엇인가?"]

        질문을 분리한 결과를 항상 리스트 형태로만 반환하라.

        ### 입력 : {query}
        ### 출력 :


        """
    )
    return prompt