import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# === Carrega variáveis de ambiente ===
load_dotenv()
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback")

# === Configuração da autenticação ===
scope = "user-read-private,user-read-email"
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
    show_dialog=True
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# === Configuração da interface ===
st.set_page_config(page_title="Moodify 🎭", page_icon="🎵", layout="centered")
st.title("🎭 Moodify — Recomendador de Músicas por Humor")
st.write("Selecione seu humor atual e receba recomendações musicais personalizadas!")

# === Seleção de humor ===
humor = st.selectbox(
    "Como você está se sentindo hoje?",
    ["Feliz 😄", "Triste 😢", "Calmo 😌", "Energético ⚡", "Apaixonado 💖", "Ansioso 😰"]
)

# === Mapeamento de humor para gêneros Spotify ===
mapa_humor = {
    "Feliz 😄": ["pop", "dance", "party"],
    "Triste 😢": ["acoustic", "piano", "sad"],
    "Calmo 😌": ["chill", "ambient", "lofi"],
    "Energético ⚡": ["rock", "electronic", "workout"],
    "Apaixonado 💖": ["romance", "rnb", "soul"],
    "Ansioso 😰": ["lofi", "ambient", "classical"]
}

# === Botão de recomendação ===
if st.button("🎧 Gerar Recomendações"):
    generos = mapa_humor[humor]
    st.write(f"**Humor selecionado:** {humor}")
    st.write("Gerando recomendações musicais com base no seu estado emocional...")

    try:
        recomendacoes = sp.recommendations(seed_genres=generos, limit=10)
        tracks = recomendacoes["tracks"]

        for faixa in tracks:
            nome = faixa["name"]
            artista = faixa["artists"][0]["name"]
            preview = faixa["preview_url"]
            capa = faixa["album"]["images"][0]["url"]

            st.image(capa, width=200)
            st.markdown(f"**{nome}** — {artista}")
            if preview:
                st.audio(preview)
            st.markdown("---")

    except Exception as e:
        st.error(f"Erro ao gerar recomendações: {e}")
