import streamlit as st
from Pages import Home, Scrittoio, Bacheca

# --- CONFIGURAZIONE STREAMLIT ---
st.set_page_config(page_title="Poeticamente", page_icon="🖋️", layout="wide")

# --- STILE CSS GLOBALE ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap');
.stApp { background-color: #fdf5e6 !important; color: #2b1d0e !important; font-family: 'EB Garamond', serif !important; }
.poetic-title { font-family: 'Playfair Display', serif; font-size: 4rem; text-align: center; color: #1a1a1a; margin-top: -40px; }
.stButton button { background-color: #2b1d0e !important; color: #fdf5e6 !important; border: 1px solid #d4af37 !important; font-family: 'Playfair Display', serif !important; border-radius: 0px !important; }
.stTextArea textarea { background-color: rgba(255,255,255,0.2) !important; border: 1px solid #d4af37 !important; font-size: 1.2rem !important; }
#MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR PER NAVIGAZIONE ---
st.sidebar.title("Menu")
page = st.sidebar.radio("Vai a:", ["Home", "Scrittoio", "Bacheca"])

if page == "Home":
    Home.show()
elif page == "Scrittoio":
    Scrittoio.show()
elif page == "Bacheca":
    Bacheca.show()