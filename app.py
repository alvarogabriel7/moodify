import os
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# --- Config (leitura de secrets no Cloud ou .env local) ---
load_dotenv()  # apenas para ambiente local se quiser usar .env

CLIENT_ID = st.secrets.get("SPOTIPY_CLIENT_ID") or os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = st.secrets.get("SPOTIPY_CLIENT_SECRET") or os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = st.secrets.get("SPOTIPY_REDIRECT_URI") or os.getenv("SPOTIPY_REDIRECT_URI") or "https://moodifyagcl.streamlit.app/callback"

if not CLIENT_ID or not CLIENT_SECRET:
    st.error("Spotify credentials missing. Add them to Streamlit Secrets or .env.")
    st.stop()

# --- OAuth config ---
SCOPE = "user-read-private user-read-email"  # suficiente para recomendações
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=".cache",   # cache local do token (no Cloud funciona também)
    open_browser=False
)

st.set_page_config(page_title="Moodify 🎭", page_icon="🎵", layout="centered")
st.title("🎭 Moodify — Recomendador de Músicas por Humor")
st.write("Selecione seu humor, conecte ao Spotify (se ainda não), e gere recomendações.")

# --- Função para obter access token (captura 'code' da URL após redirect) ---
def get_access_token_from_query():
    if "token_info" in st.session_state:
        token_info = st.session_state["token_info"]
        return token_info.get("access_token") if isinstance(token_info, dict) else token_info

    params = st.query_params
    if "code" in params:
        code = params["code"]
        try:
            token_info = auth_manager.get_access_token(code)
        except Exception as e:
            st.error(f"Erro ao trocar code por token: {e}")
            return None
        st.session_state["token_info"] = token_info
        st.query_params.clear()
        return token_info.get("access_token") if isinstance(token_info, dict) else token_info

    return None


# --- Se não tem token, mostrar link para conectar ---
access_token = get_access_token_from_query()
if not access_token:
    auth_url = auth_manager.get_authorize_url()
    st.markdown("### Primeiro passo: conectar sua conta Spotify")
    st.markdown(f"[🔗 Conectar ao Spotify]({auth_url})", unsafe_allow_html=True)
    st.info("Após login, o Spotify vai redirecionar de volta ao app. Então volte e clique em 'Gerar Recomendações'.")
    # interrompe execução até token existir
    st.stop()

# --- Inicializa cliente Spotify com o token do usuário ---
sp = spotipy.Spotify(auth=access_token)

# --- Mapeamento humor -> gêneros (ajuste conforme preferir) ---
mapa_humor = {
    "Feliz 😊": ["pop", "dance", "party"],
    "Triste 😢": ["acoustic", "sad", "piano"],
    "Relaxado 😌": ["chill", "ambient", "lofi"],
    "Energético ⚡": ["rock", "electronic", "workout"],
    "Romântico 💕": ["romance", "rnb", "soul"]
}

humor_escolhido = st.selectbox("Como você está se sentindo hoje?", list(mapa_humor.keys()))
st.write(f"Humor selecionado: **{humor_escolhido}**")

if st.button("🎧 Gerar Recomendações"):
    generos = mapa_humor[humor_escolhido]
    st.info(f"Gerando recomendações usando gêneros: {generos}")

    try:
        # Recomendações (usa o token do usuário)
        recs = sp.recommendations(seed_genres=generos, limit=10, country="BR")
        tracks = recs.get("tracks", [])

        if not tracks:
            st.warning("Nenhuma recomendação encontrada. Tente outro humor ou atualize a página.")
        else:
            st.subheader("🎶 Recomendações")
            for t in tracks:
                nome = t["name"]
                artistas = ", ".join([a["name"] for a in t["artists"]])
                capa = t["album"]["images"][0]["url"] if t["album"]["images"] else None
                preview = t.get("preview_url")
                url = t["external_urls"]["spotify"]

                cols = st.columns([1, 3])
                with cols[0]:
                    if capa:
                        st.image(capa, use_column_width=True)
                with cols[1]:
                    st.markdown(f"**[{nome}]({url})**  \n{artistas}")
                    if preview:
                        st.audio(preview)
                    st.markdown("---")

    except Exception as e:
        st.error(f"Erro ao gerar recomendações: {e}")
        # logs adicionais úteis (aparecerão nos logs do Streamlit Cloud)
        st.write("Debug: verifique logs do app no painel do Streamlit Cloud.")
