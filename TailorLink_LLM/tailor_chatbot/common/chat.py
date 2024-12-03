from openai import OpenAI  # API 통신용 모듈
import time

# OpenAI 클라이언트 초기화 함수
def get_client():
    return OpenAI()

# LLM 응답 생성 함수
def response_from_llm(prompt, message_history=None, model_id="gpt-4o-mini"):
    """
    LLM에서 스트리밍 방식으로 응답을 생성합니다.
    """
    if message_history is None:
        message_history = []

    if len(message_history) == 0:
        # 최초 질문
        message_history.append(
            {
                "role": "assistant",
                "content": "You are a helpful assistant. You must answer in Korean.",
            }
        )

    # 사용자 질문 추가
    message_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    # OpenAI 클라이언트에서 스트리밍 응답 생성
    streaming = get_client().chat.completions.create(
        model=model_id,
        messages=message_history,
        stream=True
    )

    # 스트리밍 데이터 반환
    for chunk in streaming:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
            time.sleep(0.05)
