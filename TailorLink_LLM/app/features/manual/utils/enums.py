from enum import Enum

class EmbeddingModelType(Enum):
    """
    임베딩 모델 타입 Enum.
    """
    BGE_M3 = "bge-m3"
    OPENAI = "openai"