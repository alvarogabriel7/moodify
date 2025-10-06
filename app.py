# app.py
import os
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

st.set_page_config(page_title="Moodify 🎧", layout="centered")
st.title("🎧 Moodify — Recomendações por Humor")

# ==========================
# Config (use st.secrets no Cloud)
# ==========================
CLIENT_ID = st.secrets.get("SPOTIPY_CLIENT_ID") or os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = st.secrets.get("SPOTIPY_CLIENT_SECRET") or os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = "https://moodifyagcl.streamlit.app/callback"  # keep this exact on Spotify dashboard
SCOPE = "user-read-private user-read-email"

if not CLIENT_ID or not CLIENT_SECRET:
    st.error("Credenciais Spotify faltando. Configure SPOTIPY_CLIENT_ID e SPOTIPY_CLIENT_SECRET em Streamlit Secrets.")
    st.stop()

# ==========================
# OAuth manager
# ==========================
auth_manager = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=".cache",   # permite cache local do token
    open_browser=False
)

# --------------------------
# Função utilitária para obter access_token robustamente
# --------------------------
def get_access_token_from_state_or_query():
    # 1) se já existe token em session_state, tenta usar
    token_info = st.session_state.get("token_info")
    if token_info:
        if isinstance(token_info, dict):
            return token_info.get("access_token")
        return token_info

    # 2) tenta token em cache via auth_manager (se disponível)
    try:
        cached = auth_manager.get_cached_token()
        if cached:
            st.session_state["token_info"] = cached
            return cached.get("access_token") if isinstance(cached, dict) else cached
    except Exception:
        # alguns ambientes/versões podem não expor get_cached_token; ignora
        pass

    # 3) tenta capturar 'code' vindo do redirect do Spotify (st.query_params)
    params = st.query_params
    code_param = params.get("code")
    if code_param:
        # st.query_params pode retornar lista ou string
        code = code_param[0] if isinstance(code_param, (list, tuple)) else code_param
        # trocar o code por token
        try:
            # dependendo da versão do spotipy, get_access_token pode aceitar diferentes assinaturas
            try:
                token_info = auth_manager.get_access_token(code)
            except TypeError:
                # fallback se assinatura diferente
                token_info = auth_manager.get_access_token(code, check_cache=False)
        except Exception as e:
            st.error(f"Erro ao trocar code por token: {e}")
            return None

        # token_info pode ser dict com 'access_token' ou apenas string
        st.session_state["token_info"] = token_info
        # limpa query string para não repetir troca
        st.experimental_set_query_params()
        return token_info.get("access_token") if isinstance(token_info, dict) else token_info

    # sem token
    return None

# ==========================
# Fluxo de autenticação / conexão
# ==========================
access_token = get_access_token_from_state_or_query()

if not access_token:
    auth_url = auth_manager.get_authorize_url()
    st.markdown("### Primeiro passo: conectar sua conta Spotify")
    st.markdown(f"[🔗 Conectar ao Spotify]({auth_url})", unsafe_allow_html=True)
    st.info("Após autorizar no Spotify, você será redirecionado de volta; então recarregue/pressione 'Gerar Recomendações'.")
    st.stop()

# Criar cliente Spotipy com token (garante header Authorization)
sp = spotipy.Spotify(auth=access_token)

# ==========================
# Mapeamento humor -> gêneros (valores candidatos)
# ==========================
mapa_humor = {
    "Feliz 😊": ["pop", "dance", "party"],
    "Triste 😢": ["acoustic", "piano", "singer-songwriter"],
    "Relaxado 😌": ["chill", "ambient", "lo-fi"],
    "Energético ⚡": ["rock", "electronic", "work-out"],
    "Romântico 💖": ["r-n-b", "soul", "romance"]
}

humor = st.selectbox("Como você está se sentindo hoje?", list(mapa_humor.keys()))
st.write(f"Humor selecionado: **{humor}**")

# ==========================
# Gerar recomendações
# ==========================
if st.button("🎧 Gerar Recomendações"):
    candidatos = mapa_humor.get(humor, ["pop"])
    st.info(f"Gêneros candidatos: {', '.join(candidatos)}")

    # Debug curto: mostrar se temos token (apenas parte)
    try:
        safe_token_preview = access_token[:10] + "..." + access_token[-8:]
        st.write(f"Token presente (preview): {safe_token_preview}")
    except Exception:
        pass

    # 1) obter lista de gêneros válidos diretamente da API (necessita token válido)
    try:
        seeds = sp.recommendation_genre_seeds()
    except spotipy.exceptions.SpotifyException as e:
        st.error(f"Erro ao consultar gêneros válidos: {e}")
        st.write("Verifique logs no Streamlit Cloud e se o token está válido e com o redirect URI correto.")
        st.stop()
    except Exception as e:
        st.error(f"Erro inesperado ao buscar gêneros válidos: {e}")
        st.stop()

    generos_validos_api = seeds.get("genres", []) if isinstance(seeds, dict) else []
    st.write(f"Gêneros válidos (ex.: {', '.join(generos_validos_api[:10])})")  # só exemplo

    # 2) filtrar candidatos para aqueles reconhecidos pela API
    generos_filtrados = [g for g in candidatos if g in generos_validos_api]
    if not generos_filtrados:
        st.warning("Nenhum dos gêneros mapeados para esse humor é válido segundo a API. Usando fallback 'pop'.")
        generos_filtrados = ["pop"]

    st.info(f"Enviando para recommendations: {generos_filtrados}")

    # 3) chamar recommendations com market e limit
    try:
        recs = sp.recommendations(seed_genres=generos_filtrados[:5], limit=10, market="BR")
    except spotipy.exceptions.SpotifyException as e:
        st.error(f"Erro ao gerar recomendações (SpotifyException): {e}")
        st.write("Verifique os logs do app no Streamlit Cloud; pode haver problema com token/caching.")
        st.stop()
    except Exception as e:
        st.error(f"Erro inesperado ao gerar recomendações: {e}")
        st.stop()

    tracks = recs.get("tracks", [])
    if not tracks:
        st.warning("Nenhuma faixa retornada nas recomendações.")
    else:
        st.success("Recomendações geradas:")
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
