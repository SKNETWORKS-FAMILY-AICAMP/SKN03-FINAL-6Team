from langchain_text_splitters import RecursiveCharacterTextSplitter

def text_split(docs, chunk_size=500, chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_documents = text_splitter.split_documents(docs)
    print(f"분할된 청크의수 : {len(split_documents)}")
    return split_documents