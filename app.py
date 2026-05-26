import streamlit as st
from langchain_core.messages import HumanMessage
from src.graph.builder import compilar_grafo

# 1. Configuração visual da página
st.set_page_config(page_title="Care Plus - Triagem", page_icon="🩺", layout="centered")
st.title("🩺 Care Plus - Atendimento Virtual")
st.markdown("Bem-vindo ao sistema de triagem inteligente. Como posso ajudar você hoje?")

# 2. Carrega o LangGraph (o @st.cache_resource evita que o RAG recarregue a cada mensagem)
@st.cache_resource
def carregar_sistema():
    return compilar_grafo()

app = carregar_sistema()

# 3. Cria a memória da conversa na tela
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Exibe o histórico de mensagens anteriores
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Caixa de texto onde o paciente digita
if prompt := st.chat_input("Digite seus sintomas ou dúvidas médicas..."):
    
    # Imprime a mensagem do paciente na tela e salva no histórico
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mostra um "carregando" enquanto o modelo de 120B pensa
    with st.chat_message("assistant"):
        with st.spinner("Analisando protocolos clínicos..."):
            
            # Envia a mensagem para o seu LangGraph
            estado_inicial = {"messages": [HumanMessage(content=prompt)]}
            config = {"configurable": {"thread_id": "sessao_web"}}
            
            resultado = app.invoke(estado_inicial, config)
            
            # Pega a última resposta gerada pelo sistema (Triagem, Supervisor ou Escalada)
            resposta_final = resultado['messages'][-1].content
            
            # Imprime na tela e salva no histórico
            st.markdown(resposta_final)
            st.session_state.messages.append({"role": "assistant", "content": resposta_final})