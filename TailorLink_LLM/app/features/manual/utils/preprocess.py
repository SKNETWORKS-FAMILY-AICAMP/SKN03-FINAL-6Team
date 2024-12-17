def clean_text(text):
    # 간단한 전처리 예제
    return text.replace("\n", " ").strip()

def chunk_text(text, chunk_size=100, overlap=20, max_length=500):
    """
    텍스트를 청크로 나눕니다.

    Args:
        text (str): 청크로 나눌 텍스트.
        chunk_size (int): 각 청크의 최대 단어 수.
        overlap (int): 청크 간의 중복 단어 수.
        max_length (int): 각 청크의 최대 문자열 길이.

    Returns:
        list: 나눠진 텍스트 청크 리스트.
    """
    words = text.split()  # 단어 단위로 나누기
    chunks = []
    buffer = []  # 임시 버퍼

    for i in range(0, len(words), chunk_size - overlap):
        # 현재 청크 생성
        buffer.extend(words[i:i + chunk_size])  # 이전 청크의 초과된 부분 포함
        chunk = " ".join(buffer)

        # 현재 청크가 max_length를 초과하는 경우
        while len(chunk) > max_length:
            # max_length까지만 자르고 단어 단위로 분리
            valid_chunk = chunk[:max_length].rsplit(' ', 1)[0]
            chunks.append(valid_chunk)  # 유효한 청크 저장

            # 남은 단어를 다시 버퍼에 저장
            buffer = chunk[len(valid_chunk):].strip().split()
            chunk = " ".join(buffer)  # 새로운 청크로 만듦

        # 현재 청크가 max_length 이하이면 저장하고 버퍼 비움
        if chunk:
            chunks.append(chunk)
            buffer = []

    # 남은 텍스트가 있으면 추가
    if buffer:
        chunks.append(" ".join(buffer))

    return chunks
