from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


def faiss_db():
    
    ollama_embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    loaded_db = FAISS.load_local(
        folder_path="faiss_db",
        index_name="meritz_index",
        embeddings=ollama_embeddings,
        allow_dangerous_deserialization=True,
    )
    
    
    return loaded_db