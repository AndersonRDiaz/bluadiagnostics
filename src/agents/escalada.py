from src.graph.state import BluaState
from langchain_core.messages import AIMessage

def invocar_escalada(state: BluaState):
    """
    Agente de Escalada: Acionado quando um risco à vida é detectado.
    Responsável por encerrar a sessão e registrar o alerta no log do sistema.
    """
    print("🚨 [ESCALADA] Protocolo de Emergência Iniciado.")
    
    # Simulação de registro em log de auditoria da Care Plus
    paciente_id = state.get("paciente_id", "Desconhecido")
    print(f"📄 [AUDITORIA] Registrando escalada humana para o paciente {paciente_id}...")
    
    mensagem_alerta = AIMessage(
        content="⚠️ Protocolo de segurança ativado. Por favor, desconsidere esta triagem. Procure o pronto-socorro mais próximo ou ligue para o SAMU (192) imediatamente."
    )
    
    return {
        "messages": [mensagem_alerta],
        "proximo_agente": "Fim" 
    }