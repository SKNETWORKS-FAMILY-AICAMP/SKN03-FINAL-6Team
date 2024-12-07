# recommend_car/apps/retrieval.py
import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

def search_documents(query: str, k: int = 3):
    docs = vectorstore.similarity_search(query, k=k)
    return [doc.page_content for doc in docs]
