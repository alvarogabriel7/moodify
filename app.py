import streamlit as st
import requests
from io import BytesIO

# Configurações da página
st.set_page_config(
    page_title="Moodify 🎧",
    page_icon="🎵",
    layout="centered",
)

st.title("🎧 Moodify – Músicas para o momento certo.")

st.write(
    "Escolha o seu humor e receba **três recomendações** com base nele. "
    "**Ouça direto aqui no app!** 🎶"
)


# !!! DEVIDO UM ERRO NO MEU TOKEN DA API, AS MUSICAS FORAM LISTADAS ABAIXO PARA FIM
# DE EXEMPLIFICAR COMO FICARÁ NO PROJETO FINAL. (PARA VERIFICAR A ESTRUTURA ORIGINAL, OLHAR OS COMMITS ANTERIORES) 

musicas_por_humor = {
    "Feliz 😊": [
        {
            "titulo": "Happy – Pharrell Williams",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b273c5466c6e9c69a1a2c0c9f2f0",
            "link": "https://open.spotify.com/track/60nZcImufyMA1MKQY3dcCH",
            "embed": "https://open.spotify.com/embed/track/60nZcImufyMA1MKQY3dcCH",
        },
        {
            "titulo": "Can't Stop The Feeling – Justin Timberlake",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b2734ab6a54e9a890c0f26a3a15b",
            "link": "https://open.spotify.com/track/6JV2JOEocMgcZxYSZelKcc",
            "embed": "https://open.spotify.com/embed/track/6JV2JOEocMgcZxYSZelKcc",
        },
        {
            "titulo": "Walking on Sunshine – Katrina & The Waves",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b2737df2a99596b0e93a1a93f8a3",
            "link": "https://open.spotify.com/track/2H1z8YJKl3fT2uU3R5gG2L",
            "embed": "https://open.spotify.com/embed/track/2H1z8YJKl3fT2uU3R5gG2L",
        },
    ],
    "Triste 😢": [
        {
            "titulo": "Someone Like You – Adele",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b273b7f0c8a9f39b9f2e1d1a2f9b",
            "link": "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB",
            "embed": "https://open.spotify.com/embed/track/4kflIGfjdZJW4ot2ioixTB",
        },
        {
            "titulo": "Fix You – Coldplay",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b2731c5f3e90f8dfefdf56dc9f0d",
            "link": "https://open.spotify.com/track/7LVHVU3tWfcxj5aiPFEW4Q",
            "embed": "https://open.spotify.com/embed/track/7LVHVU3tWfcxj5aiPFEW4Q",
        },
        {
            "titulo": "Let Her Go – Passenger",
            #"imagem": "https://i.scdn.co/image/ab67616d0000b273a4d5f9d6c254a4e8c2d94f18",
            "link": "https://open.spotify.com/track/0JXXNGljqupsJaZsgSbMZV",
            "embed": "https://open.spotify.com/embed/track/0JXXNGljqupsJaZsgSbMZV",
        },
    ],
    "Relaxado 😌": [
        {
            "titulo": "Weightless – Marconi Union",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b273efb4a6cbf28fdb70b6a0d7f5",
            "link": "https://open.spotify.com/track/6kKypY5VZ9pWv6DUhX7gBF",
            "embed": "https://open.spotify.com/embed/track/6kKypY5VZ9pWv6DUhX7gBF",
        },
        {
            "titulo": "Ocean Eyes – Billie Eilish",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b273bb2a10a3d2e9f9b2bcb97476",
            "link": "https://open.spotify.com/track/7hDVYcQq6MxkdJGweuCtl9",
            "embed": "https://open.spotify.com/embed/track/7hDVYcQq6MxkdJGweuCtl9",
        },
        {
            "titulo": "Banana Pancakes – Jack Johnson",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b2731a5b8762e2f44d1f0d85a6c7",
            "link": "https://open.spotify.com/track/4dVpf9jZjcORqGTLUaeYj9",
            "embed": "https://open.spotify.com/embed/track/4dVpf9jZjcORqGTLUaeYj9",
        },
    ],
    "Energético ⚡": [
        {
            "titulo": "Blinding Lights – The Weeknd",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b2733df97c7c7e5a3e16ef44b8d5",
            "link": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
            "embed": "https://open.spotify.com/embed/track/0VjIjW4GlUZAMYd2vXMi3b",
        },
        {
            "titulo": "Don't Start Now – Dua Lipa",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b27376eeca7ccf2a0a8e1d4d4a14",
            "link": "https://open.spotify.com/track/3PfIrDoz19wz7qK7tYeu62",
            "embed": "https://open.spotify.com/embed/track/3PfIrDoz19wz7qK7tYeu62",
        },
        {
            "titulo": "Uptown Funk – Bruno Mars ft. Mark Ronson",
           # "imagem": "https://i.scdn.co/image/ab67616d0000b273e1f3d9e7d18fbc50e65acb5a",
            "link": "https://open.spotify.com/track/32OlwWuMpZ6b0aN2RZOeMS",
            "embed": "https://open.spotify.com/embed/track/32OlwWuMpZ6b0aN2RZOeMS",
        },
    ],
}


# Interface

humor = st.selectbox("Como você está se sentindo hoje?", list(musicas_por_humor.keys()))

if st.button("🎶 Gerar recomendações"):
    st.subheader(f"🎧 Músicas recomendadas para o humor: {humor}")
    recomendacoes = musicas_por_humor[humor]

    for musica in recomendacoes:
        try:
            response = requests.get(musica["imagem"])
            if response.status_code == 200:
                st.image(BytesIO(response.content), width=200)
            else:
                st.warning("Não foi possível carregar a imagem da música.")
        except Exception as e:
            st.warning(f"Erro ao carregar imagem: {e}")

        st.markdown(f"**{musica['titulo']}**")
        st.markdown(f"[Ouvir no Spotify 🎧]({musica['link']})")

        # Player embutido
        st.components.v1.iframe(musica["embed"], height=80)
        st.markdown("---")

st.caption("Moodify - Desenvolvido por Álvaro Gabriel ;)")


