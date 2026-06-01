import os
from dotenv import load_dotenv
from src.graph.state import BluaState
from langchain_core.messages import AIMessage, SystemMessage
from langchain_ollama import ChatOllama
from src.rag.retriever import buscar_contexto_clinico
# IMPORTAÇÃO SEGURA: Busca a lista centralizada para evitar importação circular
from src.tools.lista_tools import tools_disponiveis

load_dotenv()

def obter_llm_remoto():
    """Inicializa o modelo configurado para uso das tools."""
    llm = ChatOllama(
        base_url="https://api.ollama.com",
        model="gpt-oss:120b",
        temperature=0.0,  # Zera a criatividade para evitar alucinação clínica
        top_p=0.1         # Foca no vocabulário mais provável
    )
    
    return llm

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
    
    # --- O CHECK DE OURO APLICADO AQUI ---
    # Ensina ao LLM quais ferramentas ele pode usar nesta rodada
    llm_com_tools = llm.bind_tools(tools_disponiveis)
    
    # Injeção dinâmica do prompt modular com RAG
    prompt_completo = f"{carregar_prompt_triagem()}\n\nPROTOCOLOS CLÍNICOS RELEVANTES:\n{contexto_clinico}"
    mensagem_sistema = SystemMessage(content=prompt_completo)
    
    # MANTENDO A MEMÓRIA: Passamos o SystemMessage + Todo o histórico da conversa
    mensagens_para_llm = [mensagem_sistema] + state["messages"]
    
    # --- INVOCANDO O MODELO CORRETO ---
    # Usamos a variável 'llm_com_tools' em vez da 'llm' original
    resposta_modelo = llm_com_tools.invoke(mensagens_para_llm)
    
    # Tratamento de Retorno
    if resposta_modelo.tool_calls:
        print(f"🛠️ [TRIAGEM] O modelo decidiu acionar ferramentas: {[t['name'] for t in resposta_modelo.tool_calls]}")
        return {
            "messages": [resposta_modelo],
            "proximo_agente": "ExecutadorTools",
            "contexto_rag": dados_rag["contexto_llm"],
            "agente_ativo": "Triagem" # Salvando o RAG no estado global
        }
    
    # --- 2. TRATAMENTO DE TEXTO E ROTEAMENTO INTELIGENTE ---
    print("✅ [TRIAGEM] Geração de texto concluída com sucesso.")
    
    # Avalia o conteúdo para decidir o próximo passo (Guardrails)
    texto_resposta = resposta_modelo.content.lower()
    proximo_passo = "Fim" # Padrão é devolver para o usuário responder

    # Se o LLM foi instruído no prompt a usar palavras-chave como [ESCALADA] ou [PRESCRIÇÃO]
    if "escalada" in texto_resposta or "red flag" in texto_resposta:
        proximo_passo = "Escalada"
    elif "prescrição" in texto_resposta or "receita" in texto_resposta:
        proximo_passo = "Prescricao"

    # Anexamos as fontes formatadas
    fontes_formatadas = f"\n\n*(Fontes consultadas: {', '.join([os.path.basename(f) for f in fontes])})*"
    mensagem_final = AIMessage(content=resposta_modelo.content + fontes_formatadas)
    
    return {
        "messages": [mensagem_final],
        "proximo_agente": proximo_passo,
        "contexto_rag": dados_rag["contexto_llm"] # Salvando o RAG no estado global
    }