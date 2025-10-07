# Moodify: Músicas para o momento certo.
Moodify é uma aplicação Web desenvolvida com Python e Streamlit que recomenda músicas com base no estado emocional do usuário.
A proposta é oferecer uma experiência personalizada, conectando sentimentos e trilhas sonoras — afinal, a música é a linguagem da alma.
# Acesse a aplicação aqui: https://moodifyagcl.streamlit.app

# 💡 Com integração à API do Spotify!
O Moodify foi desenvolvido com integração direta à API do Spotify através da biblioteca Spotipy.
Nela, o usuário pode: Fazer login com sua conta do Spotify; Permitir que o app acessasse seus gêneros musicais preferidos; Receber recomendações dinâmicas de músicas baseadas no humor selecionado e Criar playlists personalizadas diretamente em sua conta do Spotify.
Essa integração utilizava o Spotify OAuth 2.0, recuperando o access token de cada sessão autenticada e consumindo os endpoints de recomendação da API 

# 🧩 Tecnologias utilizadas na versão original:

- Python 3.13
- Streamlit
- Spotipy (API Wrapper do Spotify)
- Requests

# 🚀 Como executar o projeto localmente?

- Clone o repositório:
    git clone https://github.com/seuusuario/moodify.git
    cd moodify

- Crie e ative um ambiente virtual (opcional, mas recomendado):
    python -m venv venv
    source venv/bin/activate  # no Windows: venv\Scripts\activate

- Instale as dependências:
    pip install -r requirements.txt

- Execute o app:
    streamlit run app.py

- Acesse o app:
    O Streamlit exibirá um link local (geralmente http://localhost:8501).

# 🛠️ Estrutura do Projeto:
moodify/
│
├── app.py              # Código principal do aplicativo Streamlit
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo

# 💻 Tecnologias e Ferramentas

Streamlit
 – Framework para criação de apps interativos em Python
Spotify for Developers
 – API usada na versão original
Spotipy
 – Biblioteca Python para acesso à API do Spotify
Requests
 – Requisições HTTP simples e eficientes

# 👩‍💻 Idealizador

Álvaro Gabriel C. Lima (agcl@cin.ufpe.br)
💼 Desenvolvedor e entusiasta de design
📍 Projeto criado como conteúdo individual na matéria de Introdução à Multimídia.

