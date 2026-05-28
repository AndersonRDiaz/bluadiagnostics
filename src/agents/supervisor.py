from src.graph.state import BluaState
from src.guardrails.scope_validator import validar_escopo
from src.guardrails.moderation import moderar_conteudo
from src.guardrails.red_flags import detectar_red_flags_detalhado 
from langchain_core.messages import AIMessage

def invocar_supervisor(state: BluaState):
    print("👔 [SUPERVISOR] Analisando o estado da prancheta...")
    
    mensagem = state["messages"][-1].content

    # 1. Aplicação dos Guardrails de Entrada (Escopo e Moderação)
    if not moderar_conteudo(mensagem) or not validar_escopo(mensagem):
        print("🚫 [SUPERVISOR] Conteúdo fora de escopo ou ofensivo. Encerrando.")
        # Adicionando um aviso para a interface não ficar em silêncio
        alerta = AIMessage(content="Desculpe, só posso ajudar com questões médicas respeitosas relacionadas à Care Plus.")
        return {"messages": [alerta], "proximo_agente": "Fim"}

    # 2. Guardrail de Red Flags Dinâmico
    # O supervisor agora varre a mensagem usando o nosso novo dicionário rico
    detalhes_red_flag = detectar_red_flags_detalhado(mensagem)

    if detalhes_red_flag["red_flag_detectada"]:
        severidade = detalhes_red_flag.get("severidade_maxima", "emergencia").upper()
        print(f"🚨 [SUPERVISOR] {severidade} detectada! Direcionando para ESCALADA.")
        
        # Atualiza o estado com as informações ricas para o agente de escalada usar
        return {
            "red_flag_detectada": True,
            "red_flag_detalhes": detalhes_red_flag,
            "proximo_agente": "Escalada"
        }

    # 3. Roteamento Padrão
    print("👔 [SUPERVISOR] Contexto seguro. Direcionando para TRIAGEM.")
    return {"proximo_agente": "Triagem"}