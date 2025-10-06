import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ======================
# CONFIGURAÇÕES INICIAIS
# ======================
st.set_page_config(page_title="Moodify 🎵", page_icon="🎧", layout="centered")

st.title("🎧 Moodify — Recomendações por Humor")
st.write("Selecione seu humor e receba recomendações musicais do Spotify! 💚")

# ======================
# AUTENTICAÇÃO SPOTIFY
# ======================
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
    scope="user-read-private user-read-email"
))

# ======================
# DICIONÁRIO DE HUMORES
# ======================
humores = {
    "Feliz 😊": ["pop", "dance", "happy"],
    "Triste 😢": ["acoustic", "sad", "piano"],
    "Relaxado 😌": ["chill", "ambient", "lofi"],
    "Animado 💃": ["party", "electronic", "workout"],
    "Romântico 💕": ["romance", "rnb", "soul"]
}

# ======================
# INTERFACE DO USUÁRIO
# ======================
humor_escolhido = st.selectbox("Como você está se sentindo hoje?", list(humores.keys()))
st.write(f"Humor selecionado: **{humor_escolhido}**")

if st.button("🎶 Gerar Recomendações"):
    try:
        generos = humores[humor_escolhido]
        recomendacoes = sp.recommendations(seed_genres=generos, limit=10)
        
        if not recomendacoes["tracks"]:
            st.warning("Não foram encontradas recomendações para esse humor 😕")
        else:
            st.subheader("🎧 Suas recomendações musicais:")
            for i, faixa in enumerate(recomendacoes["tracks"], start=1):
                nome = faixa["name"]
                artistas = ", ".join([a["name"] for a in faixa["artists"]])
                url = faixa["external_urls"]["spotify"]
                st.markdown(f"**{i}. [{nome} — {artistas}]({url})**")
    except Exception as e:
        st.error(f"Erro ao gerar recomendações: {e}")

st.markdown("---")
st.caption("💡 *Projeto Moodify desenvolvido por Álvaro Gabriel*")
