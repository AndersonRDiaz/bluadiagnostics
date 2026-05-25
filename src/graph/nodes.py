from src.graph.state import BluaState
from src.agents.supervisor import invocar_supervisor
from src.agents.triagem import invocar_triagem
from langchain_core.messages import AIMessage

def supervisor_node(state: BluaState):
    """Nó que executa o agente Supervisor."""
    return invocar_supervisor(state)

def triagem_node(state: BluaState):
    """Nó que executa o agente de Triagem Clínica."""
    return invocar_triagem(state)

def escalada_node(state: BluaState):
    """Nó de emergência (Red Flag). Força o fim da sessão."""
    print("🚨 [ESCALADA] Ativando protocolo de emergência humano!")
    mensagem_alerta = AIMessage(
        content="⚠️ Por segurança, interrompemos esta triagem virtual. Por favor, dirija-se imediatamente ao Pronto-Socorro mais próximo ou ligue para o SAMU (192)."
    )
    return {"messages": [mensagem_alerta]}