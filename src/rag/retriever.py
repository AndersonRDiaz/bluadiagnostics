import os
from langchain_chroma import Chroma
from src.rag.embeddings import obter_embeddings

def buscar_contexto_clinico(pergunta_usuario: str):
    """Busca os top-4 documentos e retorna o contexto com as fontes para a interface."""
    
    # Blindagem de caminho: garante que sempre vai ler da pasta correta, não importa de onde você rode
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    caminho_db = os.path.join(raiz, 'data', 'chroma_db')
    
    vectorstore = Chroma(
        persist_directory=caminho_db,
        embedding_function=obter_embeddings()
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    resultados = retriever.invoke(pergunta_usuario)
    
    textos_formatados = []
    fontes_recuperadas = []
    
    for doc in resultados:
        fonte = doc.metadata.get('source', 'Desconhecido')
        fontes_recuperadas.append(fonte)
        texto = f"[Extraído de: {fonte}]\n{doc.page_content}"
        textos_formatados.append(texto)
    
    contexto_final = "\n\n---\n\n".join(textos_formatados)
    
    # Transforma em set para remover duplicatas e volta para lista
    fontes_unicas = list(set(fontes_recuperadas))
    
    return {
        "contexto_llm": contexto_final,
        "fontes_interface": fontes_unicas
    }