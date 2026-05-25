from src.graph.state import BluaState
from langchain_core.messages import AIMessage
from src.rag.retriever import buscar_contexto_clinico
from src.guardrails.red_flags import detectar_red_flags # Importe isso!

def invocar_triagem(state: BluaState):
    print("🩺 [TRIAGEM] Assumindo o atendimento...")
    ultima_mensagem = state["messages"][-1].content
    
    # 1. RAG
    contexto_clinico = buscar_contexto_clinico(ultima_mensagem)
    
    # 2. GUARDRAIL CLÍNICO (Usando seu arquivo red_flags.py)
    if detectar_red_flags(ultima_mensagem):
        print("⚠️ [TRIAGEM] Sintoma crítico detectado!")
        return {
            "red_flag_detectada": True, 
            "proximo_agente": "Supervisor" # O supervisor vai ler isso e mandar pro Escala
        }

    # 3. GERAÇÃO (Aqui você integrará o LLM/Ollama na Sprint 2 final)
    resposta_ia = f"Entendi. Com base nos protocolos (RAG), o caminho recomendado é..."
    return {
        "messages": [AIMessage(content=resposta_ia)],
        "proximo_agente": "Fim"
    }