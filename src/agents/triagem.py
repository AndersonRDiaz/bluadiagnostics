import os
from dotenv import load_dotenv
from src.graph.state import BluaState
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_community.chat_models import ChatOllama
from src.rag.retriever import buscar_contexto_clinico
from src.guardrails.red_flags import detectar_red_flags

load_dotenv()

def obter_llm_remoto():
    """Inicializa o modelo gpt-oss:120b apontando para a API externa."""
    return ChatOllama(
        base_url="https://ollama.com",
        model="gpt-oss:120b",
        headers={'Authorization': f"Bearer {os.getenv('OLLAMA_API_KEY')}"},
        temperature=0.2 # Baixa temperatura para respostas clínicas mais precisas e estáveis
    )

def invocar_triagem(state: BluaState):
    print("🩺 [TRIAGEM] Assumindo o atendimento e invocando gpt-oss:120b...")
    ultima_mensagem = state["messages"][-1].content
    
    # Execução do RAG e extração de fontes
    dados_rag = buscar_contexto_clinico(ultima_mensagem)
    contexto_clinico = dados_rag["contexto_llm"]
    fontes = dados_rag["fontes_interface"]
    
    # Guardrail Clínico de Red Flags
    if detectar_red_flags(ultima_mensagem):
        print("⚠️ [TRIAGEM] Sintoma crítico detectado!")
        return {
            "red_flag_detectada": True, 
            "proximo_agente": "Supervisor" 
        }

    # Geração Baseada em Contexto (RAG)
    llm = obter_llm_remoto()
    
    # Construção do prompt estruturado para o modelo
    mensagens_prompt = [
        SystemMessage(content=(
            "Você é o assistente virtual de triagem clínica da Care Plus. "
            "Sua função é orientar o paciente de forma empática com base estritamente nos "
            "protocolos clínicos fornecidos abaixo. Não invente informações fora do contexto.\n\n"
            f"PROTOCOLOS CLÍNICOS RELEVANTES:\n{contexto_clinico}"
        )),
        HumanMessage(content=ultima_mensagem)
    ]
    
    # Chamada real ao modelo de 120B
    resposta_modelo = llm.invoke(mensagens_prompt)
    
    # Anexamos as fontes de forma visível ao final da mensagem para validação da Frente A
    fontes_formatadas = f"\n\n*(Fontes consultadas: {', '.join([os.path.basename(f) for f in fontes])})*"
    conteudo_final = resposta_modelo.content + fontes_formatadas
    
    return {
        "messages": [AIMessage(content=conteudo_final)],
        "proximo_agente": "Fim"
    }