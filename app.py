# app.py

# --- 1. Importar bibliotecas ---
import streamlit as st
import os
# Importa as funções que lidam com a IA do arquivo ia_service.py
from ia_service import initialize_gemini_chat, get_ai_response

# --- 2. Configuração da Página Streamlit ---
st.set_page_config(page_title="Assistente VivaCare", layout="wide")

# --- 3. Título e Descrição na Interface ---
st.title("Assistente VivaCare 💚")
st.markdown("""
Bem-vindo(a) ao Assistente VivaCare.
Sou um chatbot desenvolvido para fornecer informações gerais e acessíveis sobre transplante de órgãos.
**Lembre-se: Eu sou uma inteligência artificial. As informações que forneço são gerais e não substituem a consulta e o acompanhamento de um profissional de saúde. Sempre consulte seu médico ou equipe de transplante.**
""")

# --- 4. Inicialização da Sessão de Chat da IA e Histórico da Conversa (Usando st.session_state) ---
# st.session_state permite manter o estado das variáveis entre as interações do Streamlit
if 'chat_session' not in st.session_state:
    # Se a sessão de chat da IA ainda não existe, inicializa-a
    st.session_state['chat_session'] = initialize_gemini_chat()
    # Adiciona uma mensagem inicial do assistente ao histórico (opcional)
    if st.session_state['chat_session']:
         st.session_state.setdefault('messages', []).append({"role": "assistant", "content": "Olá! Eu sou o Assistente TransplantCare. Como posso te ajudar hoje?"})
    else:
         st.session_state.setdefault('messages', []).append({"role": "assistant", "content": "Olá! Não consegui inicializar o assistente de IA. Por favor, verifique a configuração da API Key e reinicie o aplicativo."})


if 'messages' not in st.session_state:
    # Se o histórico de mensagens não existe, cria uma lista vazia
    st.session_state['messages'] = []
# Adaptei o formato do histórico para lista de dicionários para usar st.chat_message

# --- 5. Exibindo o Histórico da Conversa na Interface ---
# Itera sobre a lista de mensagens armazenadas no estado da sessão
for message in st.session_state['messages']:
    # Usa st.chat_message para formatar as mensagens como um chat visualmente
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 6. Entrada do Usuário (Caixa de Texto no Rodapé) ---
# st.chat_input cria uma barra de input fixa na parte inferior
prompt = st.chat_input("Digite sua mensagem aqui:")

# --- 7. Lógica para Processar a Entrada do Usuário (Quando o usuário envia uma mensagem) ---
# Este bloco é executado quando o usuário digita algo na caixa de input e aperta Enter
if prompt:
    # 1. Adiciona a mensagem do usuário ao histórico no estado da sessão
    st.session_state['messages'].append({"role": "user", "content": prompt})

    # 2. Exibe a mensagem do usuário imediatamente na interface
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Obtém a resposta da IA chamando a função do serviço de IA
    # Passa a sessão de chat da IA e a mensagem do usuário
    ia_response = get_ai_response(st.session_state['chat_session'], prompt)

    # 4. Adiciona a resposta da IA ao histórico no estado da sessão
    st.session_state['messages'].append({"role": "assistant", "content": ia_response})

    # 5. Exibe a resposta da IA na interface
    with st.chat_message("assistant"):
        st.markdown(ia_response)

    # Nota: Com st.chat_input e st.chat_message, o Streamlit geralmente
    # gerencia a re-execução e atualização da interface automaticamente após este bloco.
    # st.experimental_rerun() # Raramente necessário aqui, mas pode ser usado se a interface não atualizar como esperado