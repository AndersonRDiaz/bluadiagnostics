from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def buscar_contexto_clinico(pergunta_usuario: str):
    """Busca os top-3 documentos mais relevantes para a pergunta do paciente."""
    vectorstore = Chroma(
        persist_directory="data/chroma_db",
        embedding_function=OpenAIEmbeddings()
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    resultados = retriever.get_relevant_documents(pergunta_usuario)
    
    # Junta o texto dos documentos encontrados para enviar ao LLM
    contexto = "\n\n".join([doc.page_content for doc in resultados])
    return contexto