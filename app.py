import streamlit as st

# ======================
# CONFIGURAÇÃO DA PÁGINA
# ======================
st.set_page_config(
    page_title="Moodify 🎵",
    page_icon="🎧",
    layout="centered",
)

st.title("🎵 Moodify — Recomendações Musicais pelo Seu Humor")
st.write("Selecione o humor abaixo e descubra músicas que combinam com o seu momento! 💫")

# ======================
# DICIONÁRIO DE MÚSICAS
# ======================
musicas_por_humor = {
    "Feliz": [
        {
            "titulo": "Happy",
            "artista": "Pharrell Williams",
            "capa": "https://i.scdn.co/image/ab67616d0000b273d73c2cfcb2d6c62f9f7b81b8",
            "link": "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH",
        },
        {
            "titulo": "Can't Stop the Feeling!",
            "artista": "Justin Timberlake",
            "capa": "https://i.scdn.co/image/ab67616d0000b2738968c3fdb7f0e4b7e9e327f7",
            "link": "https://open.spotify.com/track/6JV2JOEocMgcZxYSZelKcc",
        },
        {
            "titulo": "Walking on Sunshine",
            "artista": "Katrina & The Waves",
            "capa": "https://i.scdn.co/image/ab67616d0000b27302b4b4e08b8a927e6cbf3b4b",
            "link": "https://open.spotify.com/track/3GfOAdcoc3X5GPiiXmpBjK",
        },
    ],

    "Triste": [
        {
            "titulo": "Someone Like You",
            "artista": "Adele",
            "capa": "https://i.scdn.co/image/ab67616d0000b273b25b40cfaf9c31a20d39e3c7",
            "link": "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB",
        },
        {
            "titulo": "Fix You",
            "artista": "Coldplay",
            "capa": "https://i.scdn.co/image/ab67616d0000b27393211e401a25f46bdbd13f2b",
            "link": "https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q",
        },
        {
            "titulo": "Let Her Go",
            "artista": "Passenger",
            "capa": "https://i.scdn.co/image/ab67616d0000b273baf25c6a61d1e64dcf1e0e2d",
            "link": "https://open.spotify.com/track/0JXXNGljqupsJaZsgSbMZV",
        },
    ],

    "Calmo": [
        {
            "titulo": "Weightless",
            "artista": "Marconi Union",
            "capa": "https://i.scdn.co/image/ab67616d0000b273c9980b486b1fcbf3fdfec55a",
            "link": "https://open.spotify.com/track/6UjfByV1lDLW0SOVQA4NAi",
        },
        {
            "titulo": "Bloom",
            "artista": "ODESZA",
            "capa": "https://i.scdn.co/image/ab67616d0000b27357cfdddf2e7e6cfa4cb70a04",
            "link": "https://open.spotify.com/track/3DQ0FON2F3Fn0Wl5bNR2DU",
        },
        {
            "titulo": "Night Owl",
            "artista": "Gerry Rafferty",
            "capa": "https://i.scdn.co/image/ab67616d0000b273c60a6e8cf3c52aab8ef37ac4",
            "link": "https://open.spotify.com/track/5ixT8rYlK0ZPZf09eE9j0S",
        },
    ],

    "Energético": [
        {
            "titulo": "Don't Start Now",
            "artista": "Dua Lipa",
            "capa": "https://i.scdn.co/image/ab67616d0000b2736f42b2ee17b1e3b059c6180b",
            "link": "https://open.spotify.com/track/6WrI0LAC5M1Rw2MnX2ZvEg",
        },
        {
            "titulo": "Blinding Lights",
            "artista": "The Weeknd",
            "capa": "https://i.scdn.co/image/ab67616d0000b273e0b40f3a4b58efb94454a26d",
            "link": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
        },
        {
            "titulo": "Levitating",
            "artista": "Dua Lipa feat. DaBaby",
            "capa": "https://i.scdn.co/image/ab67616d0000b273fbb7d58ba35cfb7fb6d99505",
            "link": "https://open.spotify.com/track/463CkQjx2Zk1yXoBuierM9",
        },
    ],

    "Reflexivo": [
        {
            "titulo": "The Night We Met",
            "artista": "Lord Huron",
            "capa": "https://i.scdn.co/image/ab67616d0000b2734d0cf61eacb5a3eae49e3f7b",
            "link": "https://open.spotify.com/track/3hRV0jL3vUpRrcy398teAU",
        },
        {
            "titulo": "Holocene",
            "artista": "Bon Iver",
            "capa": "https://i.scdn.co/image/ab67616d0000b2732e1c6765d0d0dc0a5ebf895f",
            "link": "https://open.spotify.com/track/4V6DPIpQv5oBzK0Dnt0I4x",
        },
        {
            "titulo": "Lost Stars",
            "artista": "Adam Levine",
            "capa": "https://i.scdn.co/image/ab67616d0000b273b5d1c203c66bb654e3e72df1",
            "link": "https://open.spotify.com/track/0U10zFw4GlBacOy9VDGfGL",
        },
    ],
}

# ======================
# SELEÇÃO DE HUMOR
# ======================
humor = st.selectbox(
    "Como você está se sentindo hoje?",
    list(musicas_por_humor.keys())
)

if st.button("🎶 Gerar Recomendações"):
    st.subheader(f"✨ Músicas recomendadas para o humor **{humor}**:")
    musicas = musicas_por_humor[humor]

    for musica in musicas:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.image(musica["capa"], width=100)
        with col2:
            st.markdown(
                f"**{musica['titulo']}** — {musica['artista']}  \n"
                f"[🎧 Ouvir no Spotify]({musica['link']})"
            )
        st.markdown("---")

st.markdown("Desenvolvido com 💜 por AGCL — *Moodify 2025*")
