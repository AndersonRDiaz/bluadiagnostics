import os
from dotenv import load_dotenv
from src.graph.state import BluaState
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from src.rag.retriever import buscar_contexto_clinico
from src.guardrails.red_flags import detectar_red_flags
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
    # Amarrando as ferramentas ao LLM (Requisito da Frente A)
    tools = [consultar_historico_paciente, verificar_interacoes_medicamentosas, agendar_teleconsulta]
    return llm.bind_tools(tools)

def carregar_prompt_triagem() -> str:
    """Lê os arquivos markdown de prompt e combina as instruções para evitar hard-code."""
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
    ultima_mensagem = state["messages"][-1].content
    
    dados_rag = buscar_contexto_clinico(ultima_mensagem)
    contexto_clinico = dados_rag["contexto_llm"]
    fontes = dados_rag["fontes_interface"]
    
    if detectar_red_flags(ultima_mensagem):
        print("⚠️ [TRIAGEM] Sintoma crítico detectado! Roteando direto para Escalada.")
        return {
            "red_flag_detectada": True, 
            "proximo_agente": "Escalada" 
        }

    llm = obter_llm_remoto()
    
    # Injeção dinâmica do prompt modular e dos dados do RAG
    mensagens_prompt = [
        SystemMessage(content=f"{carregar_prompt_triagem()}\n\nPROTOCOLOS CLÍNICOS RELEVANTES:\n{contexto_clinico}"),
        HumanMessage(content=ultima_mensagem)
    ]
    
    resposta_modelo = llm.invoke(mensagens_prompt)
    fontes_formatadas = f"\n\n*(Fontes consultadas: {', '.join([os.path.basename(f) for f in fontes])})*"
    
    if getattr(resposta_modelo, 'tool_calls', None):
        nome_ferramenta = resposta_modelo.tool_calls[0]['name']
        print(f"🛠️ [TRIAGEM] O modelo decidiu acionar a ferramenta: {nome_ferramenta}")
        
        aviso_tool = f"*(Ação do sistema: Consultando {nome_ferramenta}...)*\nPor favor, aguarde um instante enquanto verifico seus dados."
        conteudo_final = aviso_tool + fontes_formatadas
        
        return {
            "messages": [AIMessage(content=conteudo_final)],
            "proximo_agente": "Supervisor" 
        }
    else:
        print("✅ [TRIAGEM] Geração de texto concluída com sucesso.")
        conteudo_final = resposta_modelo.content + fontes_formatadas
        
        return {
            "messages": [AIMessage(content=conteudo_final)],
            "proximo_agente": "Fim"
        }