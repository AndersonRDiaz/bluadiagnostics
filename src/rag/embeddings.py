from langchain_community.embeddings import OllamaEmbeddings

def obter_embeddings():
    """Retorna o modelo de embedding local (Ollama)."""
    return OllamaEmbeddings(
        model="nomic-embed-text" 
    )