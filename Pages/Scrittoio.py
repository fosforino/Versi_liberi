import streamlit as st
from supabase import create_client

def show():
    # --- Estetica ---
    st.markdown("""
        <style>
        .stApp { background-color: #f5f5dc; }
        h1, h2, h3, p, label { font-family: 'Georgia', serif; color: #2c3e50; }
        </style>
        """, unsafe_allow_html=True)

    # --- Connessione ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "user" in st.session_state:
        user_id = st.session_state.user.id
        user_email = st.session_state.user.email

        st.title("✒️ Lo Scrittoio")

        # --- Recupero Opere ---
        try:
            res = supabase.table("Opere").select("*").eq("user_id", user_id).order("creato_il", desc=True).execute()
            opere = res.data
        except:
            opere = []

        scelta = st.sidebar.selectbox("Carica opera:", ["Nuova Opera"] + [o['titolo'] for o in opere])
        opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
        
        v_titolo = opera_corrente['titolo'] if opera_corrente else ""
        v_testo = opera_corrente['contenuto'] if opera_corrente else ""
        v_cat = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"

        # --- Layout ---
        col1, col2 = st.columns([2, 1])
        with col1:
            titolo = st.text_input("Titolo", value=v_titolo)
        with col2:
            cats = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
            idx = cats.index(v_cat) if v_cat in cats else 0
            categoria = st.selectbox("Categoria", cats, index=idx)

        contenuto = st.text_area("Versi", value=v_testo, height=400)

        if st.button("💾 Salva nel Registro"):
            dati = {
                "user_id": user_id,
                "titolo": titolo,
                "contenuto": contenuto,
                "categoria": categoria,
                "autore_email": user_email
            }
            if opera_corrente:
                supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
            else:
                supabase.table("Opere").insert(dati).execute()
            st.success("Salvato!")
            st.rerun()
    else:
        st.warning("Accedi dalla Home.")

if __name__ == "__main__":
    show()