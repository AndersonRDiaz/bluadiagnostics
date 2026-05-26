from src.graph.state import BluaState
from src.agents.supervisor import invocar_supervisor
from src.agents.triagem import invocar_triagem
from src.agents.prescricao import invocar_prescricao # <--- Importação adicionada
from langchain_core.messages import AIMessage

def supervisor_node(state: BluaState):
    """Nó que executa o agente Supervisor."""
    return invocar_supervisor(state)

def triagem_node(state: BluaState):
    """Nó que executa o agente de Triagem Clínica."""
    return invocar_triagem(state)

def prescricao_node(state: BluaState): 
    """Nó que executa o agente de Prescrição."""
    return invocar_prescricao(state)

def escalada_node(state: BluaState):
    """Nó de emergência (Red Flag). Força o fim da sessão."""
    print("🚨 [ESCALADA] Ativando protocolo de emergência humano!")
    mensagem_alerta = AIMessage(
        content="⚠️ Por segurança, interrompemos esta triagem virtual. Por favor, dirija-se imediatamente ao Pronto-Socorro mais próximo ou ligue para o SAMU (192)."
    )
    # Adicionamos o "proximo_agente": "Fim" para garantir que o grafo saiba que deve encerrar
    return {"messages": [mensagem_alerta], "proximo_agente": "Fim"}