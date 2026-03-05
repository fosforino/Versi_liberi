import streamlit as st
from supabase import create_client

# --- CONFIGURAZIONE SUPABASE ---
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(URL, KEY)

def show():
    st.header("Bacheca 🖋️")
    st.write("Qui puoi vedere tutte le poesie pubblicate dagli utenti:")

    # Recuperiamo solo i campi essenziali
    res = supabase.table("Poesie").select("titolo, versi, autore").order("creat_ad", desc=True).execute()
    poemi = res.data if res.data else []

    for p in poemi:
        st.markdown(f"**{p['titolo']}** - *{p['autore']}*")
        st.text(p['versi'])
        st.markdown("---")