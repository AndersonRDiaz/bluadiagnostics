import os
from dotenv import load_dotenv
from src.graph.state import BluaState
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
# IMPORTAÇÃO SEGURA: Busca a lista centralizada para evitar o erro de ModuleNotFound
from src.tools.lista_tools import tools_disponiveis

load_dotenv()

def obter_llm_remoto():
    """Inicializa o modelo gpt-oss:120b apontando para a API externa."""
    return ChatOllama(
        base_url="https://api.ollama.com",
        model="gpt-oss:120b",
        headers={'Authorization': f"Bearer {os.getenv('OLLAMA_API_KEY')}"},
        temperature=0.1 # Temperatura mínima para garantir a estruturação rígida do relatório
    )

def invocar_prescricao(state: BluaState):
    print("💊 [PRESCRIÇÃO] Analisando caso para rascunho de prescrição...")
    
    llm = obter_llm_remoto()
    llm_com_tools = llm.bind_tools(tools_disponiveis) # O Check de Ouro!
    
    # Injetando as orientações no prompt
    prompt_sistema = SystemMessage(content=(
        "Você é o agente de Prescrição Remota da Care Plus. "
        "Antes de gerar o rascunho da prescrição, você DEVE usar a ferramenta de consultar histórico "
        "e verificar interações medicamentosas. "
        "Por fim, gere um resumo estruturado com: Sintomas, Histórico, e Prescrição Sugerida (com alerta de interações, se houver). "
        "Lembre-se: Este documento é um RASCUNHO e será revisado por um médico."
    ))
    
    mensagens_para_llm = [prompt_sistema] + state["messages"]
    
    resposta_modelo = llm_com_tools.invoke(mensagens_para_llm)
    
    # 1. Rota das Tools: Se ele precisar consultar o banco de dados
    if resposta_modelo.tool_calls:
        print(f"🛠️ [PRESCRIÇÃO] Consultando banco de dados: {[t['name'] for t in resposta_modelo.tool_calls]}")
        return {
            "messages": [resposta_modelo],
            "proximo_agente": "ExecutadorTools" ,
            "agente_ativo": "Prescricao"
        }
        
    # 2. Rota Final: Gerando o relatório de fato
    mensagem_saida = (
        f"✅ Triagem finalizada com sucesso.\n\n"
        f"📋 **Resumo enviado para análise médica:**\n{resposta_modelo.content}\n\n"
        f"Um médico da Care Plus revisará os dados acima e entrará em contato em breve."
    )
    
    return {
        "messages": [AIMessage(content=mensagem_saida)],
        "proximo_agente": "Fim"
    }