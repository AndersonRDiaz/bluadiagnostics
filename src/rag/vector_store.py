import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import Chroma
from src.rag.chunking import obter_splitter
from src.rag.embeddings import obter_embeddings

def processar_conhecimento():
    print("📂 [RAG] Processando base de conhecimento...")
    
    # Define o caminho da raiz do projeto (onde a pasta 'data' está)
    # __file__ é o próprio vector_store.py
    # subimos dois níveis para chegar na raiz do projeto (BLUADIAGNOSTICS/)
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    # O caminho agora é simples porque já estamos na raiz (BLUADIAGNOSTICS)
    caminho_dados = os.path.join(raiz, "data", "knowledge_base")
    caminho_db = os.path.join(raiz, 'data', 'chroma_db')
    
    print(f"🔍 Buscando documentos em: {caminho_dados}")
    
    # Carrega os arquivos
    loader = DirectoryLoader(caminho_dados, glob="**/*.md", loader_cls=TextLoader)
    docs = loader.load()
    
    # Fragmenta usando nossa estratégia
    splitter = obter_splitter()
    docs_quebrados = splitter.split_documents(docs)
    
    # Vetoriza e Salva
    vectorstore = Chroma.from_documents(
        documents=docs_quebrados,
        embedding=obter_embeddings(),
        persist_directory=caminho_db
    )
    print(f"[RAG] Base indexada com {len(docs_quebrados)} fragmentos em {caminho_db}.")