from pydantic import BaseModel, Field

class QuestionList(BaseModel):
    vailid_question: bool = Field(description="제네시스 차량 관련 질문 여부")
    print_test: str = Field(description='출력 텍스트')
    question_list: list = Field(description="복합 질문 분리")
