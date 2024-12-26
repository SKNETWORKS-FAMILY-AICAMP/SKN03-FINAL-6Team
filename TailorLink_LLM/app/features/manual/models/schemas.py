from pydantic import BaseModel, Field

class QuestionList(BaseModel):
    vailid_question: bool = Field(description="제네시스 차량 관련 질문 여부")
    reason: str = Field(description='판단 이유')
    print: str = Field(description='출력 텍스트')
    question_list: list = Field(description="복합 질문 분리")

class GradeHallucinations(BaseModel):
    """Binary score for hallucination present in generation answer."""

    binary_score: str = Field(
        description="Answer is grounded in the facts, 'yes' or 'no'"
    )

class AnswerWithHistory(BaseModel):
    binary_score: str = Field(
        description="이전 대화 내용으로 응답 가능 여부, 'yes' or 'no'"
    )
    answer: str = Field(description='이전 대화 내용으로 생성한 답.')