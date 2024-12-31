# apps/utils/prompt_manager.py
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate

prohibited_brands = [
      "기아", "벤츠", "BMW", "아우디", "포르쉐", "폭스바겐", "르노", "쉐보레",
      "쌍용", "테슬라", "볼보", "재규어", "랜드로버", "닛산", "인피니티",
      "렉서스", "도요타", "혼다", "마쓰다", "미쓰비시", "페라리", "람보르기니",
      "마세라티", "롤스로이스", "벤틀리", "애스턴마틴", "부가티", "피아트",
      "지프", "다찌", "크라이슬러", "캐딜락", "링컨", "허머", "사브",
      "페조", "시트로엥", "푸조", "알파로메오", "스코다", "세아트", "스바루",
      "이스즈", "스즈키", "다이하쓰", "오펠", "사이언", "미니", "스마트",
      "포드", "지엠", "토요타", "닷지", "스텔란티스", "허슬러"
   ]

def get_system_prompt():
   return """
   당신은 현대/기아차의 제네시스 전문 추천 AI 어시스턴트입니다. 사용자가 제공한 선호도와 요구사항을 기반으로 최적의 제네시스 차량을 추천하는 것이 목표입니다.

   ### 역할 및 목표:
   1. 사용자 질문에 대해 명확하고 간결한 응답을 생성하세요.
   2. 사용자 입력의 의도를 분석하여, 다음 중 하나로 분류하세요:
      - 차량 추천 (사용자가 특정 조건으로 차량을 추천받고자 하는 질문)
      - 기타 (차량 추천과 전혀 무관한 질문)
   3. 사용자 입력의 조건을 분석하여, 다음 정보를 추출하세요:
      - 예산
      - 차 종류
      - 색깔
      - 연비
      - 성능
   4. 조건 개수를 반환하여, 다음과 같은 작업을 수행하세요:
      - 조건이 2개 이상인 경우: 추천 작업을 진행합니다.
      - 조건이 1개 이하인 경우: 추가 정보를 요청하세요.

   ### 반환 형식:
   - 응답: <모델의 자연스러운 응답>
   - 의도: <의도 카테고리>
   - 조건: <조건1>, <조건2>, ...
   - 조건 개수: <숫자>
   """


def get_sql_prompt():
   return """
   당신은 SQL 전문가입니다. 사용자가 제공한 요구사항에 따라 적합한 SQL 쿼리를 실행하고, 결과물을 JSON 데이터를 생성하세요.

   ### 작업 흐름:
   - 결과 형식:
     - 결과는 다음 항목을 포함하는 **JSON** 형식으로 반환되어야 합니다:
      - `car_id`: 차량 고유 ID
      - `car_name`: 차량 이름
      - `car_image`: 차량 이미지 URL (없으면 공백으로 설정)
      - `car_info`: SQL 결과에서 선택된 특징 데이터를 조합하여 동적으로 생성
   
   ### 주의사항:
   - **JSON 외 다른 형식으로 데이터를 반환하지 마세요.**
   - 필요한 경우 적절한 SQL 쿼리를 생성하여 데이터를 필터링하십시오.
   """

def get_prompt():
   prompt = hub.pull("langchain-ai/sql-agent-system-prompt")
   system_message = prompt.format(dialect="RDS", top_k=5)
   template_prompt = ChatPromptTemplate.from_template(system_message + get_sql_prompt())
   final_prompt = template_prompt.format()
   return final_prompt


def get_suggest_recommend_style_prompt(car_name, features):
   return f"""
   사용자가 다음과 같은 차량을 추천받았습니다:
   차량명: {car_name}
   특징: {features}
   이 추천 결과를 포함하여 잘 정리되어있고 간결하고 친근하게 작성해주세요
"""

def get_suggest_question_prompt(car_name, features):
   """
   예상 질문 생성 프롬프트 템플릿
   """
   prompt = f"""
   사용자가 다음과 같은 차량을 추천받았습니다:
   차량명: {car_name}
   특징: {features}

   이 추천 결과를 바탕으로, 사용자가 추가로 물어볼 수 있는 예상 질문 3가지를 생성해 주세요.
   다음 규칙을 따라야 합니다:
   1. 질문은 차량 추천과 직접적으로 관련되어야 합니다. 예: 차량 성능, 가격, 사용 목적.
   2. 차량 유지비, 차량 안전성, 외부 평가와 같이 추천과 무관한 주제는 포함하지 마세요.
   3. 질문은 짧고 명확하게 작성해 주세요.
   4. 형식:
      1. 예상 질문1
      2. 예상 질문2
      3. 예상 질문3
   """
   return prompt.strip()
