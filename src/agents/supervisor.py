from src.graph.state import BluaState
from src.guardrails.scope_validator import validar_escopo
from src.guardrails.moderation import moderar_conteudo

def invocar_supervisor(state: BluaState):
    print("👔 [SUPERVISOR] Analisando o estado da prancheta...")
    
    # Pegamos a última mensagem enviada pelo usuário
    mensagem = state["messages"][-1].content

    # 1. Aplicação dos Guardrails de Entrada
    if not moderar_conteudo(mensagem) or not validar_escopo(mensagem):
        print("🚫 [SUPERVISOR] Conteúdo fora de escopo ou ofensivo. Encerrando.")
        return {"proximo_agente": "Fim"}

    # 2. Guardrail de Red Flags
    if state.get("red_flag_detectada") == True:
        print("🚨 [SUPERVISOR] Emergência detectada! Direcionando para ESCALADA.")
        return {"proximo_agente": "Escalada"}

    # 3. Roteamento Padrão
    print("👔 [SUPERVISOR] Contexto seguro. Direcionando para TRIAGEM.")
    return {"proximo_agente": "Triagem"}