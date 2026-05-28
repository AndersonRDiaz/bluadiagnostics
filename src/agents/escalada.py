from src.graph.state import BluaState
from langchain_core.messages import AIMessage

def invocar_escalada(state: BluaState):
    """
    Agente de Escalada: Acionado quando um risco à vida é detectado.
    Responsável por encerrar a sessão e registrar o alerta no log do sistema,
    utilizando o contexto clínico detalhado do módulo de red flags.
    """
    print("🚨 [ESCALADA] Protocolo de Emergência Iniciado.")
    
    # Simulação de registro em log de auditoria da Care Plus
    paciente_id = state.get("paciente_id", "Desconhecido")
    
    # Recupera os detalhes da red flag salvos no estado do LangGraph
    detalhes_red_flag = state.get("red_flag_detalhes") or {}
    
    # Extrai dados para o Log de Auditoria
    protocolo = detalhes_red_flag.get("protocolo_escalada", "GERAL_192")
    categorias = ", ".join(detalhes_red_flag.get("categorias_ativadas", ["desconhecida"]))
    termos = ", ".join(detalhes_red_flag.get("termos_encontrados", []))
    
    print(f"📄 [AUDITORIA] Registrando escalada humana para o paciente {paciente_id}...")
    print(f"⚠️ [LOG CLÍNICO] Categorias: {categorias} | Gatilhos: {termos} | Protocolo: {protocolo}")
    
    # Define a mensagem para o paciente de forma dinâmica
    # Se não houver orientação específica, usa a sua mensagem padrão de fallback
    texto_orientacao = detalhes_red_flag.get(
        "orientacao", 
        "Protocolo de segurança ativado. Por favor, desconsidere esta triagem. Procure o pronto-socorro mais próximo ou ligue para o SAMU (192) imediatamente."
    )
    
    mensagem_alerta = AIMessage(
        content=f"⚠️ {texto_orientacao}"
    )
    
    # Corrigido o erro de sintaxe '{s' para '{'
    return {
        "messages": [mensagem_alerta],
        "proximo_agente": "Fim" 
    }