def clean_text(text):
    # 간단한 전처리 예제
    return text.replace("\n", " ").strip()

def chunk_text(text, chunk_size=100, overlap=20):
    """
    텍스트를 청크로 나눕니다.

    Args:
        text (str): 청크로 나눌 텍스트.
        chunk_size (int): 각 청크의 최대 길이.
        overlap (int): 청크 간의 중복 길이.

    Returns:
        list: 나눠진 텍스트 청크 리스트.
    """
    words = text.split()  # 단어 단위로 나누기
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks
