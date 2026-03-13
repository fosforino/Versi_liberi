import streamlit as st
from supabase import create_client

def show():
    st.markdown("<style>.stApp { background-image: url('https://www.transparenttextures.com/patterns/parchment.png') !important; }</style>", unsafe_allow_html=True)
    
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    st.markdown("<h1>🏛️ Bacheca Poetica</h1>", unsafe_allow_html=True)

    try:
        res = supabase.table("Opere").select("*").order("creato_il", desc=True).execute()
        opere = res.data or []
        for o in opere:
            st.markdown(f"""
            <div style="background:#fffaf0; padding:20px; border:1px solid #c19a6b; margin-bottom:20px; border-radius:5px; box-shadow: 2px 2px 8px rgba(0,0,0,0.1);">
                <div style="font-family:'EB Garamond'; font-size:1.6rem; color:#3e2723; font-weight:bold;">{o['titolo']}</div>
                <div style="color:#8d6e63; font-style:italic;">Poeta: {o['autore_email']}</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander("Leggi il manoscritto"):
                st.write(o['contenuto'])
    except Exception as e:
        st.error("Il calamaio è momentaneamente vuoto o la connessione è interrotta.")