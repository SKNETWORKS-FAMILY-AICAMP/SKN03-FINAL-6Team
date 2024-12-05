

# 단계 5: 검색기(Retriever) 생성
# 문서에 포함되어 있는 정보를 검색하고 생성합니다.
def get_retriever(vectorstore):
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    return retriever