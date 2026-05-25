from src.graph.state import BluaState
from langchain_core.messages import AIMessage

def invocar_prescricao(state: BluaState):
    """
    Agente de Prescrição: Prepara o relatório para o médico humano validar.
    NUNCA prescreve autonomamente (Mitigação de risco clínico).
    """
    print("💊 [PRESCRIÇÃO] Preparando resumo para validação médica...")
    
    # Aqui, no futuro, ele consultaria o RAG para sugestões baseadas nos protocolos
    resumo_triagem = "Resumo clínico estruturado para validação médica."
    
    mensagem = AIMessage(
        content=f"✅ Triagem finalizada. {resumo_triagem} Um médico da Care Plus revisará seu caso e entrará em contato em breve via app."
    )
    
    return {
        "messages": [mensagem],
        "proximo_agente": "Fim"
    }