import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

# ==============================
# CONFIGURAÇÕES DA PÁGINA
# ==============================
st.set_page_config(page_title="Moodify 🎵", page_icon="🎧", layout="centered")

st.title("🎵 Moodify – Recomendações musicais baseadas no seu humor")

# ==============================
# CREDENCIAIS (do .streamlit/secrets.toml)
# ==============================
CLIENT_ID = st.secrets["SPOTIPY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIPY_CLIENT_SECRET"]
REDIRECT_URI = "https://moodifyagcl.streamlit.app/callback"  # deve ser o mesmo configurado no painel do Spotify

SCOPE = "user-read-private user-read-email user-top-read playlist-modify-public"

# ==============================
# AUTENTICAÇÃO SPOTIFY
# ==============================
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
)

# ==============================
# FUNÇÃO PARA GERENCIAR TOKEN
# ==============================
def get_access_token_from_state_or_query():
    # 1️⃣ Se já temos o token guardado
    if "token_info" in st.session_state and st.session_state["token_info"]:
        token_info = st.session_state["token_info"]
        return token_info.get("access_token")

    # 2️⃣ Se o Spotify redirecionou com um código
    query_params = st.query_params
    if "code" in query_params:
        # o Streamlit agora retorna query_params como um dicionário simples
        code = query_params["code"]
        token_info = auth_manager.get_access_token(code)
        st.session_state["token_info"] = token_info
        # limpa a query string
        st.query_params.clear()
        return token_info.get("access_token")

    # 3️⃣ Nenhum token encontrado
    return None


# ==============================
# FLUXO DE LOGIN
# ==============================
access_token = get_access_token_from_state_or_query()

if not access_token:
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"[🔑 Conectar ao Spotify]({auth_url})")
    st.stop()

sp = spotipy.Spotify(auth=access_token)

# ==============================
# INTERFACE DE HUMOR
# ==============================
st.subheader("Como você está se sentindo hoje?")
humor = st.selectbox(
    "Selecione seu humor",
    ["Feliz", "Triste", "Relaxado", "Energético", "Romântico"]
)

# ==============================
# MAPA DE HUMOR → GÊNEROS
# ==============================
mapa_humor_generos = {
    "Feliz": ["pop", "dance", "party"],
    "Triste": ["acoustic", "sad", "piano"],
    "Relaxado": ["chill", "ambient", "lofi"],
    "Energético": ["rock", "workout", "edm"],
    "Romântico": ["romance", "rnb", "soul"]
}

# ==============================
# GERAR RECOMENDAÇÕES
# ==============================
if st.button("🎧 Gerar recomendações"):
    try:
        generos = mapa_humor_generos.get(humor, ["pop"])
        sp = spotipy.Spotify(auth=access_token)

        # Solicita recomendações com base no humor
        recomendacoes = sp.recommendations(seed_genres=generos, limit=10, market="BR")

        if recomendacoes and recomendacoes["tracks"]:
            st.success("✨ Aqui estão suas recomendações!")
            for faixa in recomendacoes["tracks"]:
                nome = faixa["name"]
                artistas = ", ".join([art["name"] for art in faixa["artists"]])
                link = faixa["external_urls"]["spotify"]
                st.markdown(f"🎶 [{nome} – {artistas}]({link})")
        else:
            st.warning("Nenhuma recomendação encontrada para esse humor 😢")

    except Exception as e:
        st.error(f"Erro ao gerar recomendações: {e}")
        st.info("⚙️ Dica: verifique se o token de acesso não expirou. Caso tenha expirado, reconecte-se ao Spotify.")

# ==============================
# RODAPÉ
# ==============================
st.markdown("---")
st.caption("Desenvolvido com ❤️ e ☕ por Álvaro Gabriel – Projeto Moodify")
