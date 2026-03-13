import streamlit as st
from supabase import create_client
import pydantic
from Pages import Scrittoio, Bacheca

def apply_global_style():
    st.markdown("""
    <style>
        /* SFONDO VERDINO SMERALDO DELICATO */
        .stApp {
            background-color: #e0f2f1 !important; 
            background-image: none !important; 
        }

        /* TITOLI E TESTI */
        h1, h2, h3, label, .stMarkdown {
            color: #004d40 !important;
            font-family: 'Playfair Display', serif;
        }

        /* INPUT E CAMPI DI TESTO */
        input, .stTextInput > div > div > input {
            background-color: #ffffff !important;
            border: 2px solid #b2dfdb !important;
            color: #004d40 !important;
            border-radius: 8px !important;
        }

        /* BOTTONI 3D SMERALDO */
        div.stButton > button {
            background-color: #4db6ac !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: bold !important;
            text-transform: uppercase;
            box-shadow: 0 6px 0 #00796b !important;
            transition: all 0.1s ease-in-out !important;
        }

        div.stButton > button:active {
            box-shadow: 0 2px 0 #00796b !important;
            transform: translateY(4px) !important;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    apply_global_style()
    
    if "utente" not in st.session_state:
        st.session_state.utente = None

    st.sidebar.title("Navigazione")
    pagina = st.sidebar.radio("Vai a:", ["Home", "Scrittoio", "Bacheca"])

    if pagina == "Home":
        st.markdown("<h1 style='text-align: center;'>🎨 Poeticamente</h1>", unsafe_allow_html=True)
        # Qui va la tua logica di login...
    elif pagina == "Scrittoio":
        Scrittoio.show()
    elif pagina == "Bacheca":
        Bacheca.show()

if __name__ == "__main__":
    main()