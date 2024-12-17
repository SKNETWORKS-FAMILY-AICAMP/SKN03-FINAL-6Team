from pymilvus.model.reranker import BGERerankFunction

bge_rf = BGERerankFunction(
    model_name="BAAI/bge-reranker-v2-m3",  # Specify the model name. Defaults to `BAAI/bge-reranker-v2-m3`.
    device="cpu" # Specify the device to use, e.g., 'cpu' or 'cuda:0'
)
