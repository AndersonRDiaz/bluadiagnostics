from langchain_community.embeddings import OllamaEmbeddings

def obter_embeddings():
    """Retorna o modelo de embedding rodando localmente (leve), evitando o erro 404 do servidor."""
    return OllamaEmbeddings(
        model="nomic-embed-text" 
    )