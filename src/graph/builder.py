from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from src.graph.state import BluaState
from src.graph.nodes import supervisor_node, triagem_node, escalada_node, prescricao_node

# IMPORTAR A SUA FUNÇÃO DE GUARDRAIL
from src.tools.consultar_historico import consultar_historico_paciente
from src.tools.verificar_interacoes import verificar_interacoes_medicamentosas
from src.tools.agendar_teleconsulta import agendar_teleconsulta

# Agora o Python sabe quem são essas funções e não vai dar NameError
tools_disponiveis = [consultar_historico_paciente, verificar_interacoes_medicamentosas, agendar_teleconsulta]
executador_tools_node = ToolNode(tools_disponiveis)

def roteamento_dinamico(state: BluaState):
    """
    Função universal de roteamento.
    Como os nós já processaram a lógica e definiram qual é o próximo passo
    no campo 'proximo_agente', a aresta só precisa ler e obedecer.
    """
    return state.get("proximo_agente", END)


def compilar_grafo():
    workflow = StateGraph(BluaState)
    
    # Adiciona todos os nós da arquitetura
    workflow.add_node("Supervisor", supervisor_node)
    workflow.add_node("Triagem", triagem_node)
    workflow.add_node("Escalada", escalada_node)
    workflow.add_node("Prescricao", prescricao_node)
    workflow.add_node("ExecutadorTools", executador_tools_node) # <-- Agora o nó existe!
    
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

    # Se o Executador de Tools terminar, ele devolve a resposta para a Triagem analisar
    workflow.add_edge("ExecutadorTools", "Triagem")
    
    # Fim dos processos
    workflow.add_edge("Escalada", END)
    workflow.add_edge("Prescricao", END)

    memoria = MemorySaver()
    return workflow.compile(checkpointer=memoria)