from src.graph.state import BluaState
from src.guardrails.scope_validator import validar_escopo
from src.guardrails.moderation import moderar_conteudo
from src.guardrails.red_flags import detectar_red_flags_detalhado 
from langchain_core.messages import AIMessage

def invocar_supervisor(state: BluaState):
    print("👔 [SUPERVISOR] Analisando o estado da prancheta...")
    
    mensagem = state["messages"][-1].content

    moderacao = moderar_conteudo(mensagem)
    escopo = validar_escopo(mensagem)

    print(f"🔍 [DEBUG] moderacao={moderacao}")
    print(f"🔍 [DEBUG] escopo={escopo}")
    print(f"🔍 [DEBUG] mensagem='{mensagem[:150]}'")

    # Aplicação dos Guardrails de Entrada (Escopo e Moderação)
    if not moderacao or not escopo:
        print("🚫 [SUPERVISOR] Conteúdo fora de escopo ou ofensivo. Encerrando.")
        alerta = AIMessage(content="Desculpe, só posso ajudar com questões médicas relacionadas à Care Plus.")
        return {"messages": [alerta], "proximo_agente": "Fim"}

    # Guardrail de Red Flags Dinâmico
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
    
    palavras_prescricao = ["prescri", "remédio", "medicamento", "receita", "pós-consulta", "pos-consulta"]
    if any(p in mensagem.lower() for p in palavras_prescricao):
        print("💊 [SUPERVISOR] Intent de prescrição detectada.")
        return {"proximo_agente": "Prescricao"}

    # 3. Roteamento Padrão
    print("👔 [SUPERVISOR] Contexto seguro. Direcionando para TRIAGEM.")
    return {"proximo_agente": "Triagem"}