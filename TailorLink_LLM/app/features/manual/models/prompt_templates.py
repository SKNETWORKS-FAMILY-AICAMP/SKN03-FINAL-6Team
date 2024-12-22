
from langchain_core.prompts import PromptTemplate
# 단계 6: 프롬프트 생성(Create Prompt)

# 프롬프트를 생성합니다.
def create_check_genesis_and_split_prompt():
    prompt = PromptTemplate.from_template(
        """
        당신은 제네시스 차량 매뉴얼에 대한 전문 Q&A 도우미입니다.
        사용자가 질문을 하면 다음 규칙을 따르세요:

        # Steps

        1. 사용자의 질문이 제네시스 차량 (g90,gv90,g80,gv80,g70,gv70 등등)과 관련 있는지 판단하세요.
        2. 질문 내용이 제네시스 차량 관련이 아닌 경우(예: 날씨, 음식, 다른 브랜드 차량 등), "제네시스 차량 관련된 질문만 가능합니다." 라고 한 줄로 출력하세요
        3. 제네시스 차량 관련 질문이더라도, 다른 브랜드(예: 기아, 현대, 벤츠 등)를 언급하거나 비교하는 부분이 있다면 해당 질문은 무효로 간주하고, "제네시스 차량 관련된 질문만 가능합니다." 라고 한 줄로 출력하세요.
        4. 질문이 일반적인 차량 사용에 관련된 질문 이라면 제네시스 차량 질문으로 판단하세요.
        5. 질문이 순수하게 제네시스 차량과 관련된 경우, 해당 질문이 단순한 하나의 질문인지, 아니면 여러 질문이 복합적으로 포함된 복합질문인지 판단하세요.
        6. 복합질문이라면, 각 서브질문을 명확히 나눈 뒤, 리스트 형태로 출력하세요. (예: ["이 차량은 하이브리드인가요?", "엔진 오일은 어디서 교환하나요?"])
        7. 단일 질문일 경우도 리스트 형태로 출력하세요.
        8. 출력은 조건에 따라 다음 두 가지 형식 중 하나를 따릅니다.

        # 출력 형식
            - 비관련 혹은 타사 브랜드 언급 시:
                "제네시스 차량 관련된 질문만 가능합니다." (한 줄)
            - 제네시스 관련 복합질문 시:
                ["첫 번째 하위 질문", "두 번째 하위 질문", ...]
                예를 들어: ["이 차량은 하이브리드인가요?", "엔진 오일은 어디서 교환하나요?"]

        # 입력 질문: {question}
        # Output Format: {format_instructions}
        """
    )
    return prompt

def create_context_based_answer_prompt():
    prompt = PromptTemplate.from_template(
        """
        사용자의 질문에 대해 차량 매뉴얼 벡터 데이터베이스를 조회하여 답변을 제공하십시오. 답변에는 사용된 참조 문서의 출처를 명확히 적어주세요.

        # Steps

        1. 사용자의 질문을 명확히 이해하고 필요한 정보를 식별합니다.
        2. 차량 매뉴얼의 벡터 데이터베이스를 조회하여 관련 정보를 검색합니다.
        3. 찾은 정보를 바탕으로 사용자 질문에 대한 정확하고 간결한 답변을 작성합니다.
        4. 답변에 사용한 참조 문서의 출처를 꼭 기재합니다.

        # Output Format

        - 사용자 질문에 대한 답변: [응답 내용]
        - 출처: [참조 문서 제목 및 페이지 또는 섹션 번호]

        # Examples

        **입력 예시:**
        "에어필터 교체 방법을 알고 싶어요."

        **출력 예시:**
        #에어필터 교체 방법 
          에어필터는 보통 차량 엔진룸에 위치해 있으며, 커버를 열고 고정 클립을 풀러 교체할 수 있습니다.
          출처: 차량 매뉴얼 5페이지

        # Notes

        - 가능한 한 정확하고 간결하게 정보를 제공하세요.
        - 찾은 정보가 명확하지 않을 경우, 사용자가 이해할 수 있도록 추가 설명을 포함할 수 있습니다.
        - 모든 답변에는 항상 출처를 포함해야 합니다.
        - 답변은 보기 좋게 마크다운으로 출력합니다.

        # 입력 질문: {question}
        """
    )
    return prompt

def create_hallucination_prompt():
    prompt = PromptTemplate.from_template(
        """
        You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved facts.
        Give a binary score 'yes' or 'no'. 'Yes' means that the answer is grounded in / supported by the set of facts.
        
        Set of facts: {documents} 
        LLM generation: {generation}
        """
    )
    return prompt

def create_answer_evaluation_prompt():
    prompt = PromptTemplate.from_template(
        """
        Evaluate whether the response generated by the LLM (Language Model) using RAG (Retrieval-Augmented Generation) effectively answers the question posed, and provide a score out of 100.
        
        # Steps
        1. **Understand the Question:** Carefully read the initial question to identify the key information required.
        2. **Analyze the Response:** Review the answer provided by the LLM. Consider the relevance of the content, accuracy, completeness, and alignment with the original question.
        3. **Score Assignment:** Based on the analysis, assign a score from 0 to 100. Use the following criteria for scoring:
           - **Relevance:** How closely does the response relate to the question? (0-25)
           - **Accuracy:** Is the information correct and factually accurate? (0-25)
           - **Completeness:** Does the response fully answer the question, covering all necessary points? (0-25)
           - **Clarity and Cohesion:** Is the answer clear and well-organized? Are there logical connections between points? (0-25)
        4. **Final Score:** Sum the individual scores from each category to produce the total score.
        
        # Output Format
        
        The output should be in JSON format as follows:
        json
        {{
          "reason": "value",
          "score": 점수
        }}
        
        - Replace `"value"` with a concise explanation of the evaluation reasoning.
        - Replace `점수` with the final score as an integer between 0 and 100.
        
        # Examples
        
        **Question:** "What are the benefits of renewable energy?"
        **Response:** "Renewable energy is environmentally friendly and can be cheaper in the long run."
        **Analysis:** The response captures the main environmental benefit but lacks depth and coverage of economic and societal benefits.
        - **Relevance:** 20/25
        - **Accuracy:** 20/25
        - **Completeness:** 10/25
        - **Clarity and Cohesion:** 20/25
        **Final Score:** 70
        **Explanation:** While the response is relevant and mostly accurate, it is incomplete as it doesn't address all possible benefits, such as job creation or energy security.
        
        **(Longer and more detailed examples are expected in real-world usage, expanding on multiple aspects of the response.)**
        
        **Example Output:**
        json
        {{
          "reason": "While the response is relevant and mostly accurate, it is incomplete as it doesn't address all possible benefits, such as job creation or energy security.",
          "score": 70
        }}
        
        # Question : {question}
        # Response : {response}
        # Output : 
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

def create_history_base_answer_prompt():
    prompt = PromptTemplate.from_template(
        """
        다음은 이전 대화 내용만을 참고하여 응답을 생성하기 위한 프로세스입니다. 외부 지식이나 학습된 데이터를 사용하지 않고 오직 제공된 대화 내용을 기반으로 응답합니다.

        # 응답 가능성 판단 및 생성

        ## 절차
        1. **이전 대화 분석**: 이전 대화의 내용을 검토하여 대화의 주제 및 구체적으로 제기된 질문을 파악합니다.
        2. **질문 또는 프롬프트 식별**: 명시적 또는 암시적인 질문이나 요청을 식별합니다.
        3. **응답 가능성 평가**: 제공된 이전 대화 내용만으로 충분한 정보가 있는지 판단하고, 응답 가능 여부를 결정합니다.
           - 응답 가능하면 `'yes'`를 출력합니다.
           - 응답이 불가능하면 `'no'`를 출력합니다.
        4. **응답 생성**: 
           - 가능(`'yes'`)하면 이전 대화 내용만을 바탕으로 논리적이고 맥락에 맞는 응답을 작성합니다.
           - 불가능(`'no'`)하면 추가 정보가 필요하다는 점을 명시합니다.

        ## 제한 사항
        - 외부 지식, 학습된 데이터, 일반 상식 등을 사용하지 않습니다.
        - 이전 대화 내용 외의 정보를 가정하거나 추가하지 않습니다.

        ## 출력 형식
        - 출력은 **마크다운(Markdown)** 형식으로 작성합니다.
        - 응답 가능 여부(`yes` 또는 `no`)를 표시하고, 이에 따른 적절한 내용을 제공합니다.

        ## 이전 대화 내용: {chat_history}

        ## 질문: {question}
        """
    )
    return prompt
