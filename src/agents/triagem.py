import os
from dotenv import load_dotenv
from src.graph.state import BluaState
from langchain_core.messages import AIMessage, SystemMessage
from langchain_ollama import ChatOllama
from src.rag.retriever import buscar_contexto_clinico
from src.tools.consultar_historico import consultar_historico_paciente
from src.tools.verificar_interacoes import verificar_interacoes_medicamentosas
from src.tools.agendar_teleconsulta import agendar_teleconsulta

load_dotenv()

def obter_llm_remoto():
    """Inicializa o modelo configurado para uso das tools."""
    llm = ChatOllama(
        base_url="https://api.ollama.com",
        model="gpt-oss:120b",
        temperature=0.2
    )
    tools = [consultar_historico_paciente, verificar_interacoes_medicamentosas, agendar_teleconsulta]
    return llm.bind_tools(tools)

def carregar_prompt_triagem() -> str:
    """Lê os arquivos markdown de prompt e combina as instruções."""
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    caminho_base = os.path.join(raiz, 'prompts', 'system_prompt.md')
    caminho_agente = os.path.join(raiz, 'prompts', 'agent_triagem.md')
    caminho_few_shot = os.path.join(raiz, 'prompts', 'few_shot_examples.md')
    
    with open(caminho_base, 'r', encoding='utf-8') as f: prompt_base = f.read()
    with open(caminho_agente, 'r', encoding='utf-8') as f: prompt_agente = f.read()
    with open(caminho_few_shot, 'r', encoding='utf-8') as f: prompt_few_shot = f.read()
    
    return f"{prompt_base}\n\n{prompt_agente}\n\n{prompt_few_shot}"

def invocar_triagem(state: BluaState):
    print("🩺 [TRIAGEM] Assumindo o atendimento e invocando modelo...")
    
    # Busca o RAG usando apenas a última mensagem para manter o foco da busca
    ultima_mensagem = state["messages"][-1].content
    dados_rag = buscar_contexto_clinico(ultima_mensagem)
    contexto_clinico = dados_rag["contexto_llm"]
    fontes = dados_rag["fontes_interface"]
    
    llm = obter_llm_remoto()
    
    # Injeção dinâmica do prompt modular com RAG
    prompt_completo = f"{carregar_prompt_triagem()}\n\nPROTOCOLOS CLÍNICOS RELEVANTES:\n{contexto_clinico}"
    mensagem_sistema = SystemMessage(content=prompt_completo)
    
    # MANTENDO A MEMÓRIA: Passamos o SystemMessage + Todo o histórico da conversa
    mensagens_para_llm = [mensagem_sistema] + state["messages"]
    
    # Invoca o modelo
    resposta_modelo = llm.invoke(mensagens_para_llm)
    
    # Tratamento de Retorno
    if resposta_modelo.tool_calls:
        print(f"🛠️ [TRIAGEM] O modelo decidiu acionar ferramentas: {[t['name'] for t in resposta_modelo.tool_calls]}")
        # IMPORTANTE: Retorna a mensagem original com o payload das tools.
        # O próximo agente deve ser o nó responsável por rodar as funções Python reais.
        return {
            "messages": [resposta_modelo],
            "proximo_agente": "ExecutadorTools" 
        }
    else:
        print("✅ [TRIAGEM] Geração de texto concluída com sucesso.")
        # Se for apenas texto, anexamos as fontes e retornamos
        fontes_formatadas = f"\n\n*(Fontes consultadas: {', '.join([os.path.basename(f) for f in fontes])})*"
        
        # Cria uma nova AIMessage modificada com as fontes concatenadas
        mensagem_final = AIMessage(content=resposta_modelo.content + fontes_formatadas)
        
        return {
            "messages": [mensagem_final],
            "proximo_agente": "Fim"
        }