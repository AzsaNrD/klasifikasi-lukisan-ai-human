import streamlit as st

from src.theme import apply_theme

st.set_page_config(
    page_title="Pendeteksi Gambar Lukisan Buatan AI",
    page_icon="🎨",
    layout="wide",
)

apply_theme()

pages = [
    st.Page("views/beranda.py", title="Beranda", default=True),
    st.Page("views/histori.py", title="Histori"),
    st.Page("views/tentang_penelitian.py", title="Tentang Penelitian"),
]

navigation = st.navigation(pages, position="top")
navigation.run()
