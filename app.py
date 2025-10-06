import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

# ==========================
# CONFIGURAÇÃO DO APP
# ==========================
st.set_page_config(page_title="Moodify 🎧", page_icon="🎵", layout="centered")

st.title("🎵 Moodify — Recomendador de Músicas por Emoção")
st.write("Selecione seu humor e receba recomendações musicais personalizadas.")

# ==========================
# CONFIGURAÇÃO DO SPOTIFY
# ==========================
CLIENT_ID = st.secrets["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = st.secrets["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = "https://moodifyagcl.streamlit.app/callback"

SCOPE = "user-read-private user-read-email"

auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    show_dialog=True,
    cache_path=".spotipyoauthcache"
)

# ==========================
# FUNÇÃO DE TOKEN
# ==========================
def get_access_token_from_state_or_query():
    # 1️⃣ Se já temos token salvo em sessão e válido
    if "token_info" in st.session_state:
        token_info = st.session_state["token_info"]
        if token_info and token_info.get("expires_at", 0) > int(time.time()):
            return token_info["access_token"]
        else:
            # renova token expirado
            token_info = auth_manager.refresh_access_token(token_info["refresh_token"])
            st.session_state["token_info"] = token_info
            return token_info["access_token"]

    # 2️⃣ Se veio código pela URL (após login no Spotify)
    query_params = st.query_params
    if "code" in query_params:
        code = query_params["code"]
        token_info = auth_manager.get_access_token(code)
        st.session_state["token_info"] = token_info
        st.query_params.clear()
        return token_info["access_token"]

    return None


# ==========================
# FLUXO DE AUTENTICAÇÃO
# ==========================
access_token = get_access_token_from_state_or_query()

if not access_token:
    auth_url = auth_manager.get_authorize_url()
    st.markdown(f"[Conectar ao Spotify 🎧]({auth_url})")
    st.stop()

# Criar cliente Spotipy com o token ativo
sp = spotipy.Spotify(auth=access_token)

# ==========================
# INTERFACE — EMOÇÕES
# ==========================
moods = {
    "😎 Feliz": ["pop", "dance", "party"],
    "😔 Triste": ["acoustic", "sad", "piano"],
    "😌 Calmo": ["chill", "ambient", "lofi"],
    "🔥 Animado": ["edm", "rock", "hip-hop"],
    "💔 Reflexivo": ["singer-songwriter", "indie", "folk"]
}

selected_mood = st.selectbox("Como você está se sentindo hoje?", moods.keys())

if st.button("🎶 Gerar Recomendações"):
    with st.spinner("Buscando músicas ideais para seu humor..."):
        try:
            genres = moods[selected_mood]
            # ✅ chamada correta com token válido
            recommendations = sp.recommendations(seed_genres=genres, limit=10, market="BR")

            if not recommendations["tracks"]:
                st.warning("Nenhuma recomendação encontrada. Tente outro humor.")
            else:
                st.success("Aqui estão suas músicas recomendadas 🎧:")
                for track in recommendations["tracks"]:
                    st.write(f"**{track['name']}** — {track['artists'][0]['name']}")
                    st.audio(track["preview_url"], format="audio/mp3")

        except spotipy.exceptions.SpotifyException as e:
            st.error(f"Erro ao gerar recomendações: {e}")
            st.info("Verifique se o token ainda está ativo ou tente reconectar ao Spotify.")
