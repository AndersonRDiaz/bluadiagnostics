from langgraph.graph import StateGraph, START, END
from src.graph.state import BluaState
from src.graph.nodes import supervisor_node, triagem_node, escalada_node, prescricao_node

# 1. IMPORTAR A SUA FUNÇÃO DE GUARDRAIL
from src.guardrails.red_flags import detectar_red_flags

def roteamento_supervisor(state: BluaState):
    """Lógica que o grafo usa para decidir para onde ir após o Supervisor."""
    
    # 2. PEGAR O TEXTO DA ÚLTIMA MENSAGEM DO USUÁRIO
    if state.get("messages"):
        ultima_mensagem = state["messages"][-1].content
        
        # 3. VERIFICAR SE HÁ EMERGÊNCIA (A MÁGICA ACONTECE AQUI)
        if detectar_red_flags(ultima_mensagem):
            return "Escalada" # Se der True, desvia na hora para a emergência!

    return state.get("proximo_agente", "Triagem")

def roteamento_triagem(state: BluaState):
    """Lógica que o grafo usa após a Triagem."""
    # Prioridade máxima: Segurança (Red Flags)
    # Aqui continua funcionando, caso a IA de triagem detecte algo no meio da conversa
    if state.get("red_flag_detectada"):
        return "Escalada"
    
    # Se a triagem precisar de mais validação, devolve para o Supervisor.
    proximo = state.get("proximo_agente", "Supervisor") 
    return proximo

def compilar_grafo():
    workflow = StateGraph(BluaState)
    
    # Adiciona todos os nós
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Triagem", triagem_node)
    workflow.add_node("Escalada", escalada_node)
    workflow.add_node("Prescricao", prescricao_node)
    
    # Fluxo Inicial
    workflow.add_edge(START, "Supervisor")
    
    # Roteamento Condicional 
    workflow.add_conditional_edges(
        "Supervisor", 
        roteamento_supervisor,
        {
            "Triagem": "Triagem",
            "Escalada": "Escalada",
            "Prescricao": "Prescricao", 
            "Fim": END
        }
    )
    
    workflow.add_conditional_edges(
        "Triagem",
        roteamento_triagem,
        {
            "Escalada": "Escalada",
            "Prescricao": "Prescricao",
            "Supervisor": "Supervisor",
            "Fim": END
        }
    )
    
    # Fim dos processos
    workflow.add_edge("Escalada", END)
    workflow.add_edge("Prescricao", END)
    
    return workflow.compile()