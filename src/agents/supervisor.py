from src.graph.state import BluaState
from src.guardrails.scope_validator import validar_escopo
from src.guardrails.moderation import moderar_conteudo 
from langchain_core.messages import AIMessage # Importando o AIMessage

def invocar_supervisor(state: BluaState):
    print("👔 [SUPERVISOR] Analisando o estado da prancheta...")
    
    mensagem = state["messages"][-1].content

    # Aplicação dos Guardrails de Entrada
    if not moderar_conteudo(mensagem) or not validar_escopo(mensagem):
        print("🚫 [SUPERVISOR] Conteúdo fora de escopo ou ofensivo. Encerrando.")
        # Adicionando um aviso para a interface não ficar em silêncio
        alerta = AIMessage(content="Desculpe, só posso ajudar com questões médicas respeitosas relacionadas à Care Plus.")
        return {"messages": [alerta], "proximo_agente": "Fim"}

    # Guardrail de Red Flags
    if state.get("red_flag_detectada") == True:
        print("🚨 [SUPERVISOR] Emergência detectada! Direcionando para ESCALADA.")
        return {"proximo_agente": "Escalada"}

    # Roteamento Padrão
    print("👔 [SUPERVISOR] Contexto seguro. Direcionando para TRIAGEM.")
    return {"proximo_agente": "Triagem"}