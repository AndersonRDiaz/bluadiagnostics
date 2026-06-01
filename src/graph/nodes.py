from src.graph.state import BluaState
from src.agents.supervisor import invocar_supervisor
from src.agents.triagem import invocar_triagem
from src.agents.prescricao import invocar_prescricao 
from langchain_core.messages import AIMessage

def supervisor_node(state: BluaState):
    """Nó que executa o agente Supervisor."""
    return invocar_supervisor(state)

def triagem_node(state: BluaState):
    """Nó que executa o agente de Triagem Clínica."""
    # Executa o agente e pega o dicionário de resposta
    resultado = invocar_triagem(state)
    
    # INJEÇÃO CRÍTICA: Garante que o LangGraph saiba e memorize quem chamou a tool
    resultado["agente_ativo"] = "Triagem"
    return resultado

def prescricao_node(state: BluaState): 
    """Nó que executa o agente de Prescrição."""
    # Executa o agente e pega o dicionário de resposta
    resultado = invocar_prescricao(state)
    
    # INJEÇÃO CRÍTICA: Garante que o LangGraph saiba e memorize quem chamou a tool
    resultado["agente_ativo"] = "Prescricao"
    return resultado

def escalada_node(state: BluaState):
    """Nó de emergência (Red Flag). Força o fim da sessão."""
    print("🚨 [ESCALADA] Ativando protocolo de emergência humano!")
    mensagem_alerta = AIMessage(
        content="⚠️ Por segurança, interrompemos esta triagem virtual. Por favor, dirija-se imediatamente ao Pronto-Socorro mais próximo ou ligue para o SAMU (192)."
    )
    return {"messages": [mensagem_alerta], "proximo_agente": "Fim"}