import streamlit as st

def show():
    st.markdown("<h1 class='poetic-title'>Benvenuto in Poeticamente 🖋️</h1>", unsafe_allow_html=True)
    st.write("""
        Poeticamente è la tua piattaforma gratuita per scrivere poesie.
        
        ✅ Puoi registrarti con un **pseudonimo** per pubblicare le tue opere.  
        ✅ Tutte le poesie vengono controllate automaticamente per linguaggio corretto.  
        ✅ Puoi scaricare le tue poesie in PDF.  
        ✅ La Bacheca mostra solo titolo, autore e testo delle poesie.  
    """)