from langchain_text_splitters import RecursiveCharacterTextSplitter

def obter_splitter():
    """
    Define a estratégia de fragmentação dos documentos.
    Mantido em aprox. 1200 caracteres para garantir que fique na faixa 
    de 200-400 tokens recomendada para protocolos clínicos.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=1200,      # Tamanho ideal para protocolos médicos
        chunk_overlap=200,    # Mantém 200 caracteres de contexto entre chunks
        add_start_index=True,
    )