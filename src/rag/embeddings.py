from langchain_ollama import OllamaEmbeddings

def obter_embeddings():
    """Retorna o modelo de embedding rodando localmente, evitando o erro 404 do servidor."""
    return OllamaEmbeddings(
        model="nomic-embed-text" 
    )