from langgraph.graph import StateGraph, START, END
from src.graph.state import BluaState
from src.graph.nodes import supervisor_node, triagem_node, escalada_node, prescricao_node

def roteamento_supervisor(state: BluaState):
    """Lógica que o grafo usa para decidir para onde ir após o Supervisor."""
    # Adicionamos um fallback: se o supervisor não souber para onde ir, ele vai para a Triagem
    return state.get("proximo_agente", "Triagem")

def roteamento_triagem(state: BluaState):
    """Lógica que o grafo usa após a Triagem."""
    # Prioridade máxima: Segurança (Red Flags)
    if state.get("red_flag_detectada"):
        return "Escalada"
    
    # Roteamento baseado na decisão do agente de triagem
    proximo = state.get("proximo_agente", "Fim")
    return proximo

def compilar_grafo():
    workflow = StateGraph(BluaState)
    
    # 1. Adiciona todos os nós
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Triagem", triagem_node)
    workflow.add_node("Escalada", escalada_node)
    workflow.add_node("Prescricao", prescricao_node)
    
    # 2. Fluxo Inicial
    workflow.add_edge(START, "Supervisor")
    
    # 3. Roteamento Condicional
    workflow.add_conditional_edges(
        "Supervisor", 
        roteamento_supervisor,
        {
            "Triagem": "Triagem",
            "Escalada": "Escalada",
            "Prescricao": "Prescricao", # Adicionado para robustez
            "Fim": END
        }
    )
    
    workflow.add_conditional_edges(
        "Triagem",
        roteamento_triagem,
        {
            "Escalada": "Escalada",
            "Prescricao": "Prescricao",
            "Fim": END
        }
    )
    
    # 4. Fim dos processos
    workflow.add_edge("Escalada", END)
    workflow.add_edge("Prescricao", END)
    
    return workflow.compile()