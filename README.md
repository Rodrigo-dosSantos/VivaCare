
Assistente VivaCare 💚
Um assistente conversacional inteligente para pacientes e cuidadores de transplante de órgãos.
Sobre o Projeto
Este projeto é um chatbot desenvolvido com Inteligência Artificial Generativa (Google Gemini) e o framework Streamlit para criar uma interface gráfica amigável. O objetivo é fornecer informações acessíveis e de apoio a pessoas que passaram ou estão passando por um processo de transplante de órgãos, como pacientes, familiares e cuidadores.
O Assistente VivaCare utiliza os aprendizados da Imersão IA Alura + Google Gemini para:
Conversar de forma natural e empática.
Responder perguntas frequentes sobre cuidados gerais pós-transplante.
Utilizar ferramentas (como busca na internet) para encontrar informações mais recentes ou recursos relevantes.
(Se você implementou) Orquestrar agentes para realizar tarefas mais específicas, como buscar e formatar listas de recursos.
Importante: Este assistente é uma ferramenta de apoio informativo e não substitui o aconselhamento e acompanhamento de um profissional de saúde (médicos, nutricionistas, etc.). As informações fornecidas são geradas por IA e devem ser sempre verificadas com a equipe de saúde responsável pelo paciente.
Funcionalidades
Respostas a perguntas gerais sobre transplante de órgãos e cuidados pós-transplante.
Busca por informações recentes ou recursos (associações, ONGs, hospitais) na internet (utilizando a ferramenta Google Search).
Manutenção de histórico de conversação (na sessão atual do chat).
(Se aplicável) Lógica de orquestração para direcionar consultas específicas a agentes especializados.
Interface gráfica intuitiva baseada em chat.
Tecnologias Utilizadas
Google Gemini API: O modelo de linguagem generativa que alimenta o assistente.
Google AI SDK para Python: Biblioteca para interagir com a API Gemini.
Google ADK (Agent Development Kit): Utilizado para a criação e orquestração de agentes (se aplicou na Fase 1 - Passo 4).
Streamlit: Framework Python para a criação rápida da interface gráfica web.
Python: Linguagem de programação principal do projeto.
Git/GitHub: Controle de versão e hospedagem do código.
Como Configurar e Rodar (Localmente)
Siga estes passos para clonar o repositório e rodar o Assistente VivaCare na sua máquina:
Pré-requisitos:
Ter o Python instalado (versão 3.8 ou superior recomendado).
Ter o Git instalado.
Obter uma API Key do Google AI Studio (https://aistudio.google.com/).
Clone o Repositório: Abra o terminal e clone o código para o seu computador.
git clone [https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git)
# SUBSTITUA pela URL do seu repositório no GitHub

Entre na pasta do projeto clonado:
cd NomeDaPastaDoSeuRepositorio
# Substitua pelo nome da pasta criada pelo clone (ex: AssistenteVivaCare)


Crie e Ative o Ambiente Virtual: É altamente recomendado usar um ambiente virtual.
python -m venv venv

Ative o ambiente virtual:
No Linux/macOS:
source venv/bin/activate


No Windows (Prompt de Comando):
venv\Scripts\activate.bat


No Windows (PowerShell):
.\venv\Scripts\Activate.ps1


(Você verá (venv) no início da linha do terminal se a ativação for bem-sucedida).
Instale as Dependências: Com o ambiente virtual ativo, instale as bibliotecas necessárias a partir do arquivo requirements.txt (vamos criar este arquivo agora, veja a seção abaixo!).
pip install -r requirements.txt


Configure a Variável de Ambiente GOOGLE_API_KEY: O projeto lê a API Key de uma variável de ambiente para segurança.
Localmente (para a sessão atual do terminal):
export GOOGLE_API_KEY='SUA_CHAVE_DA_API_DO_GOOGLE_AQUI'
# SUBSTITUA SUA_CHAVE_DA_API_DO_GOOGLE_AQUI PELA SUA CHAVE REAL!
# Use aspas simples. Este comando vale apenas para a sessão atual do terminal.


(Formas mais persistentes variam por OS - veja documentação do seu sistema para configurar variáveis de ambiente globalmente ou adicione ao seu .bashrc/profile com cautela).
Rode a Aplicação Streamlit: Com o ambiente virtual ativo E a variável de ambiente configurada na mesma sessão do terminal, execute:
streamlit run app.py

(Se você encontrar problemas de sintaxe com streamlit run app.py mesmo no venv ativado, pode tentar usar o caminho completo para o executável: /caminho/completo/da/pasta/do/projeto/venv/bin/streamlit run app.py - mas tente a forma simples primeiro no ambiente ativado).
O aplicativo deve abrir no seu navegador padrão (geralmente em http://localhost:8501).
Criando o arquivo requirements.txt
Este arquivo lista as bibliotecas que seu projeto precisa para que outras pessoas possam instalá-las facilmente (Passo 10 da Reinicialização).
Abra o terminal na pasta raiz do seu projeto (onde estão app.py e ia_service.py).
Certifique-se de que seu ambiente virtual (venv) está ativo (source venv/bin/activate ou o comando equivalente para o seu OS).
Execute o comando para gerar o arquivo:
pip freeze > requirements.txt


Edite o arquivo requirements.txt: O comando pip freeze lista TUDO que está no ambiente. Abra o arquivo requirements.txt com um editor de texto e remova as bibliotecas que não são essenciais para o seu projeto funcionar. Deixe apenas:
google-genai
google-adk
streamlit
(Se seus agentes usarem, pode precisar de requests, python-dateutil, authlib, cryptography, cffi - verifique as dependências que apareceram no pip freeze e que parecem relacionadas ao google-adk ou busca). Remova bibliotecas de coisas que você não usou (ex: ipython, jupyter, colab-.*, .*display, .*warnings - coisas de ambiente de notebook).
Salve o arquivo requirements.txt.
Adicione este novo arquivo ao Git, commite e envie para o GitHub:
git add requirements.txt
git commit -m "Adiciona arquivo de requisitos"
git push origin main # Use 'master' se aplicável


Screenshots ou Demo

Possíveis Melhorias Futuras
Salvar histórico da conversa (usando banco de dados ou arquivo).
Adicionar mais tipos de agentes para tarefas específicas (ex: lembretes de medicação - com MUITA cautela e ressalvas médicas claras!, sumarizar artigos de pesquisa, etc.).
Melhorar a interface gráfica.
Deploy do aplicativo para que outros possam usar sem rodar localmente (ex: Streamlit Cloud, Hugging Face Spaces).
Agradecimentos
Um agradecimento especial à Alura e ao Google Gemini pela Imersão IA Alura + Google Gemini, que forneceu os conhecimentos e ferramentas essenciais para desenvolver este projeto.
Autor
Rodrigo dos Santos
linkedin.com/in/rodrigo-dosantos
github.com/Rodrigo-dosSantos 
