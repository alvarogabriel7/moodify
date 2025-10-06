import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# ==============================
# 🔧 CONFIGURAÇÕES DO APP
# ==============================
st.set_page_config(page_title="Moodify 🎧", page_icon="🎵", layout="centered")

# Título
st.title("🎧 Moodify — Recomendações musicais pelo seu humor")

# ==============================
# 🔐 CONFIGURAÇÃO DE CREDENCIAIS
# ==============================
SPOTIPY_CLIENT_ID = st.secrets["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = st.secrets["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = "https://moodifyagcl.streamlit.app/callback"
SCOPE = "user-library-read playlist-modify-public"

# Inicializa autenticação Spotify
auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE,
)

# ==============================
# ⚙️ AUTENTICAÇÃO
# ==============================
query_params = st.query_params
code = query_params.get("code", None)

if "token_info" not in st.session_state:
    if code:
        token_info = auth_manager.get_access_token(code, check_cache=False)
        st.session_state.token_info = token_info
    else:
        auth_url = auth_manager.get_authorize_url()
        st.markdown(
            f"[🔑 Conectar ao Spotify]({auth_url})",
            unsafe_allow_html=True,
        )
        st.stop()

# Cria cliente Spotify autenticado
sp = spotipy.Spotify(auth=st.session_state.token_info["access_token"])

# ==============================
# 🎭 ESCOLHA DO HUMOR
# ==============================
st.subheader("Como você está se sentindo hoje?")
humor = st.selectbox(
    "Selecione seu humor:",
    ["Feliz", "Triste", "Relaxado", "Motivado", "Romântico"]
)

# Mapeamento de humor → gêneros válidos do Spotify
humores_para_generos = {
    "Feliz": ["pop", "dance", "edm"],
    "Triste": ["acoustic", "piano", "singer-songwriter"],
    "Relaxado": ["chill", "ambient", "lo-fi"],
    "Motivado": ["rock", "hip-hop", "metal"],
    "Romântico": ["r-n-b", "soul", "romance"]
}

# Gêneros correspondentes ao humor selecionado
generos = humores_para_generos.get(humor, ["pop"])

# ==============================
# 🔍 BUSCAR RECOMENDAÇÕES
# ==============================
if st.button("🎶 Gerar recomendações"):
    try:
        # Filtra gêneros válidos diretamente da API
        generos_validos = sp.recommendation_genre_seeds()["genres"]
        generos_filtrados = [g for g in generos if g in generos_validos]

        if not generos_filtrados:
            st.error("Nenhum gênero válido encontrado para este humor.")
            st.stop()

        st.info(f"🎧 Gerando recomendações com base em: {', '.join(generos_filtrados)}")

        recomendacoes = sp.recommendations(seed_genres=generos_filtrados[:5], limit=10, market="BR")

        tracks = recomendacoes.get("tracks", [])
        if not tracks:
            st.warning("😕 Nenhuma recomendação encontrada. Tente outro humor.")
        else:
            st.success("✨ Aqui estão suas músicas recomendadas:")
            for track in tracks:
                nome = track["name"]
                artista = ", ".join([a["name"] for a in track["artists"]])
                url = track["external_urls"]["spotify"]
                st.markdown(f"- [{nome} – {artista}]({url})")

    except Exception as e:
        st.error(f"Erro ao gerar recomendações: {e}")
        st.write("🔍 Debug: verifique os logs no Streamlit Cloud para mais detalhes.")
