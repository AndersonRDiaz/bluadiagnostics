from langchain_text_splitters import RecursiveCharacterTextSplitter

def obter_splitter():
    """Define a estratégia de fragmentação dos documentos."""
    return RecursiveCharacterTextSplitter(
        chunk_size=1000,      # Tamanho ideal para protocolos médicos
        chunk_overlap=200,    # Mantém 200 caracteres de contexto entre chunks
        add_start_index=True,
    )