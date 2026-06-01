from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from src.graph.state import BluaState
from src.graph.nodes import supervisor_node, triagem_node, escalada_node, prescricao_node

from src.tools.lista_tools import tools_disponiveis

executador_tools_node = ToolNode(tools_disponiveis)

def roteamento_dinamico(state: BluaState):
    return state.get("proximo_agente", END)

# --- NOVA FUNÇÃO DE ROTEAMENTO PARA AS TOOLS ---
def roteamento_pos_tools(state: BluaState):
    """Lê quem chamou a tool e devolve a execução para o mesmo agente."""
    return state.get("agente_ativo", "Supervisor")

def compilar_grafo():
    workflow = StateGraph(BluaState)
    
    # Adiciona todos os nós da arquitetura
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Triagem", triagem_node)
    workflow.add_node("Escalada", escalada_node)
    workflow.add_node("Prescricao", prescricao_node)
    workflow.add_node("ExecutadorTools", executador_tools_node) 
    
    # Define o ponto de entrada
    workflow.add_edge(START, "Supervisor")
    
    # Roteamentos Condicionais
    workflow.add_conditional_edges(
        "Supervisor", 
        roteamento_dinamico,
        {
            "Triagem": "Triagem",
            "Escalada": "Escalada",
            "Prescricao": "Prescricao",
            "Fim": END
        }
    )
    
    workflow.add_conditional_edges(
        "Triagem",
        roteamento_dinamico,
        {
            "Escalada": "Escalada",
            "Supervisor": "Supervisor",
            "ExecutadorTools": "ExecutadorTools", # Triagem manda para as tools
            "Prescricao": "Prescricao",
            "Fim": END
        }
    )

    # --- NOVO: Arestas condicionais da Prescrição ---
    workflow.add_conditional_edges(
        "Prescricao",
        roteamento_dinamico,
        {
            "ExecutadorTools": "ExecutadorTools",
            "Supervisor": "Supervisor",
            "Fim": END
        }
    )

    # --- CORREÇÃO CRÍTICA DO BUg ---
    # O Executador de Tools agora usa roteamento condicional para voltar ao agente correto
    workflow.add_conditional_edges(
        "ExecutadorTools", 
        roteamento_pos_tools,
        {
            "Triagem": "Triagem",
            "Prescricao": "Prescricao",
            "Supervisor": "Supervisor"
        }
    )

    workflow.add_edge("Escalada", END)
    
    memoria = MemorySaver()
    return workflow.compile(checkpointer=memoria)