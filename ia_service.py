# ia_service.py

# --- 1. Importar bibliotecas necessárias ---
import os
from google import genai
from google.genai import types
from google.adk.tools import google_search # Importa a ferramenta de busca do ADK

# Importações para Agentes (google-adk)
from google.adk.agents import Agent
from google.adk.runners import Runner # Necessário para call_agent
from google.adk.sessions import InMemorySessionService # Necessário para call_agent
import textwrap # Para formatar texto
import warnings # Para gerenciar warnings

warnings.filterwarnings("ignore")

# --- 2. Configurar a API Key (Para ambiente local/deploy) ---
# A chave API DEVE estar configurada como variavel de ambiente GOOGLE_API_KEY
API_KEY = os.environ.get('GOOGLE_API_KEY')

if not API_KEY:
    # Se a variável de ambiente não estiver configurada, levante um erro
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está configurada. Por favor, configure-a.")

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
     print(f"ERRO FATAL: Falha ao configurar a API Key do genai. Erro: {e}")
     raise # Levanta o erro para interromper a inicialização do app

# --- 3. Definir o Modelo ---
MODEL_ID = "gemini-2.0-flash" # Modelo rápido e com bom custo-benefício. Pode testar outros se desejar.

# --- 4. Funções Auxiliares para Agentes ---
# Função para chamar um agente e obter a resposta final.
def call_agent(agent: Agent, message_text: str) -> str:
    """Envia uma mensagem para um agente e retorna a resposta final."""
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="streamlit_user", session_id="streamlit_session")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    print(f"DEBUG: Acionando agente '{agent.name}' com entrada: {message_text[:50]}...") # Para ver no terminal Streamlit
    try:
        for event in runner.run(user_id="streamlit_user", session_id="streamlit_session", new_message=content):
            if event.is_final_response():
                print(f"DEBUG: Agente '{agent.name}' retornou resposta final.")
                for part in event.content.parts:
                    if part.text is not None:
                        final_response += part.text
                        final_response += "\n"
            # Você pode adicionar feedback intermediário aqui se desejar
            # Ex: print(f"DEBUG: Agente '{agent.name}' pensou: {event.agent_thought.thought}")
            # Ex: print(f"DEBUG: Agente '{agent.name}' usou ferramenta: {event.action_request.tool_code.tool_code}")

    except Exception as e:
        print(f"ERRO: Erro durante a execução do agente {agent.name}. Erro: {e}")
        return f"Desculpe, ocorreu um erro ao executar a tarefa. (Erro no agente: {e})"
    return final_response

# --- 5. Definições de Agentes Específicos (Exemplo Implementado) ---
# ESTES SÃO AGENTES DE EXEMPLO - VOCÊ PODE ADAPTAR OU CRIAR SEUS PRÓPRIOS

def agente_buscador_recursos(termo_busca: str) -> str:
    """Define e chama um agente para buscar recursos relacionados a transplante."""
    buscador_recursos = Agent(
        name="agente_buscador_recursos",
        model=MODEL_ID, # Usa o mesmo modelo principal
        instruction="""
        Você é um assistente focado em encontrar recursos e links úteis relacionados a transplante
        usando a busca do Google (Google Search).
        Dado um termo de busca, procure por associações de pacientes, ONGs de apoio, hospitais de referência
        em transplante, ou informações de contato úteis sobre o tema no Brasil.
        Seja o mais preciso possível na busca para encontrar resultados relevantes.
        Retorne uma lista dos recursos encontrados, incluindo o nome e o link, se disponível.
        Se não encontrar nada relevante, diga que não encontrou.
        """,
        description="Agente que busca recursos de apoio a transplantados no Google.",
        tools=[google_search] # Este agente precisa da ferramenta de busca
    )
    # Chama a função auxiliar para executar este agente
    return call_agent(agente=buscador_recursos, message_text=f"Buscar recursos sobre: {termo_busca}. Foco no Brasil.")

def agente_formatador_recursos(resultados_brutos: str) -> str:
    """Define e chama um agente para formatar resultados de busca de recursos."""
    formatador = Agent(
        name="agente_formatador_recursos",
        model=MODEL_ID, # Pode usar o mesmo modelo ou um diferente se necessário
        instruction="""
        Você é um assistente que formata listas de recursos relacionados a transplante.
        Dado um texto contendo resultados de busca, formate-o em uma lista clara e organizada para um usuário.
        Inclua o nome do recurso e qualquer link ou informação de contato disponível.
        Adicione uma introdução amigável e uma conclusão que REFORCE a necessidade de verificar as informações
        diretamente com o recurso ou um profissional de saúde.
        Se os resultados brutos indicarem que nada foi encontrado, formate uma resposta informando isso.
        """,
        description="Agente que formata resultados de busca de recursos para o usuário.",
        # Este agente não precisa de ferramentas se apenas formata o texto que recebe
        tools=[]
    )
    # Chama a função auxiliar para executar este agente
    return call_agent(agent=formatador, message_text=f"Resultados de busca brutos para formatar:\n{resultados_brutos}")


# --- 6. Função de Inicialização da Sessão de Chat Principal ---
def initialize_gemini_chat():
    """Inicializa e retorna uma sessão de chat com o modelo Gemini e configuração VivaCare."""
    chat_config = types.GenerateContentConfig(
        system_instruction = """
    Você é o Assistente VivaCare, um chatbot amigável e informativo focado em fornecer informações gerais e acessíveis sobre transplante de órgãos (como fígado, rim, coração, pulmão, etc.) e cuidados pós-transplante.
    Seu objetivo principal é auxiliar pacientes, cuidadores ou pessoas interessadas com dúvidas básicas sobre o processo, recuperação, rotina e bem-estar pós-transplante.
    Sua linguagem deve ser clara, simples, empática e fácil de entender para quem não tem conhecimento médico profundo.
    Você deve manter um tom de suporte e encorajamento.

    É ABSOLUTAMENTE ESSENCIAL que, em **todas as suas respostas** que abordem temas de saúde, tratamento, medicação, sintomas, dieta, exercícios, ou qualquer conselho médico/de cuidado, você inclua a seguinte **RESSALVA DE FORMA CLARA E VISÍVEL**:

    ---
    **Importante:** Eu sou uma inteligência artificial e não substituo um profissional de saúde. As informações que forneço são para fins educacionais e de apoio geral e **não constituem aconselhamento médico**. Sempre consulte seu médico, equipe de transplante, nutricionista ou outro profissional de saúde qualificado para obter diagnóstico, tratamento, conselhos e orientações personalizadas para sua condição específica. Não tome decisões sobre sua saúde ou mude seu tratamento com base apenas nas informações que eu forneço.
    ---

    Responda apenas perguntas diretamente relacionadas a transplante de órgãos e cuidados pós-transplante. Se a pergunta for completamente fora deste tema, diga educadamente que sua especialidade é transplante e você não pode ajudar com aquele tópico.

    Não invente informações ou procedimentos médicos. Se você não tem certeza sobre algo, diga que não tem a informação ou que o usuário deve consultar um profissional.

    Esteja pronto para receber perguntas em português do Brasil.
    """
)

    # Ferramentas para o chat principal (se ele usar alguma diretamente)
    tools_for_chat = [google_search] # Exemplo: permite que o chat principal use a busca para perguntas que ele julgar apropriado

    try:
        model = genai.GenerativeModel(
            model_name=MODEL_ID,
            generation_config=chat_config,
            tools=tools_for_chat
        )
        chat_session = model.start_chat()
        print("DEBUG: Sessão de chat Gemini inicializada com sucesso.")
        return chat_session
    except Exception as e:
        print(f"ERRO FATAL: Falha ao inicializar a sessão de chat Gemini. Verifique API Key e permissões. Erro: {e}")
        return None

# --- 7. Função para Obter Resposta da IA (Inclui Lógica de Orquestração) ---
def get_ai_response(chat_session, user_message):
    """
    Processa a mensagem do usuário.
    Contém a lógica de orquestração para usar o chat principal ou agentes específicos.
    """
    if chat_session is None:
         return "O assistente de IA não foi inicializado. Por favor, verifique a configuração da API Key e reinicie o aplicativo."

    try:
        # --- LÓGICA DE ORQUESTRAÇÃO (Exemplo implementado chamando os agentes definidos acima) ---
        # Esta lógica decide O QUE fazer com a mensagem do usuário.
        # Adapte as condições (if/elif) e as chamadas de agente/chat_session conforme a sua necessidade.

        # Exemplo: Se a mensagem do usuário contiver "buscar recursos sobre", aciona a cadeia de agentes de busca e formatação
        if "buscar recursos sobre" in user_message.lower():
            print("DEBUG: Orquestração: Detectada intenção de buscar recursos. Acionando cadeia de agentes.")
            # Extrai o termo de busca da mensagem do usuário
            termo = user_message.lower().replace("buscar recursos sobre", "").strip()
            if not termo:
                 return "Por favor, especifique o tipo de recurso que você deseja buscar (ex: 'buscar recursos sobre transplante de rim')."

            # Chama o Agente Buscador de Recursos
            resultados_brutos = agente_buscador_recursos(termo)

            # Passa os resultados brutos para o Agente Formatador de Recursos
            resposta_final = agente_formatador_recursos(resultados_brutos)

            print("DEBUG: Orquestração: Resposta final da cadeia de agentes pronta.")
            return resposta_final # RETORNA a resposta formatada pelos agentes

        else:
            # Se nenhuma intenção específica para agentes foi detectada, usa o chat_session principal
            print(f"DEBUG: Orquestração: Nenhuma intenção específica detectada. Usando chat_session padrão para: {user_message[:50]}...")
            # Envia a mensagem para a sessão de chat e obtém a resposta
            response = chat_session.send_message(user_message)
            print("DEBUG: Resposta recebida do chat_session.")
            return response.text # RETORNA a resposta do chat principal

    except Exception as e:
        print(f"ERRO: Ocorreu um erro durante a interação com a IA na get_ai_response. Erro: {e}")
        # Retorna uma mensagem de erro amigável para o usuário na interface gráfica
        return "Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde."

