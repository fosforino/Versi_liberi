import streamlit as st
from supabase import create_client

def show():
    # --- STILE SPECIFICO DELLO SCRITTOIO ---
    st.markdown("""
        <style>
        /* Sfondo specifico per lo Scrittoio: Pergamena più calda */
        .stApp {
            background-color: #f4ecd8 !important;
            background-image: url("https://www.transparenttextures.com/patterns/parchment.png") !important;
        }

        /* Area di inserimento testo: Foglio di carta avorio */
        textarea, input {
            background-color: #fff9eb !important;
            border: 1px solid #c19a6b !important;
            color: #3e2723 !important;
            font-family: 'EB Garamond', serif !important;
            font-size: 1.2rem !important;
        }

        /* Menu a tendina coordinato */
        div[data-baseweb="select"] > div {
            background-color: #fff9eb !important;
            border: 1px solid #c19a6b !important;
        }

        /* BOTTONI CON EFFETTO CERALACCA / INCHIOSTRO */
        /* Bottone Salva - Verde Bosco Profondo */
        div.stButton > button[key="btn_salva"] {
            background: linear-gradient(145deg, #4b633a, #3a4d2d) !important;
            color: white !important;
            border: 1px solid #2d3a22 !important;
            border-radius: 12px !important;
            box-shadow: 3px 3px 6px rgba(0,0,0,0.3) !important;
            font-weight: bold !important;
        }

        /* Bottone Stampa - Blu Notte Inchiostro */
        div.stButton > button[key="btn_stampa"] {
            background: linear-gradient(145deg, #2c3e50, #1a252f) !important;
            color: white !important;
            border: 1px solid #141d26 !important;
            border-radius: 12px !important;
            box-shadow: 3px 3px 6px rgba(0,0,0,0.3) !important;
            font-weight: bold !important;
        }

        /* Bottone Elimina - Rosso Sangue di Drago */
        div.stButton > button[key="btn_cancella"] {
            background: linear-gradient(145deg, #a93226, #7b241c) !important;
            color: white !important;
            border: 1px solid #641e16 !important;
            border-radius: 12px !important;
            box-shadow: 3px 3px 6px rgba(0,0,0,0.3) !important;
        }

        /* Effetto al passaggio del mouse */
        div.stButton > button:hover {
            transform: translateY(-2px) !important;
            filter: brightness(1.2) !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- LOGICA SUPABASE ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" in st.session_state:
        nome_poeta = st.session_state.utente
        st.markdown(f"<h1 style='text-align: center; color: #5d4037;'>✒️ Lo Scrittoio di {nome_poeta}</h1>", unsafe_allow_html=True)

        try:
            res = supabase.table("Opere").select("*").eq("autore_email", nome_poeta).order("creato_il", desc=True).execute()
            opere = res.data
        except:
            opere = []

        scelta = st.sidebar.selectbox("📖 Carica opera:", ["Nuova Opera"] + [o['titolo'] for o in opere])
        opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
        
        v_titolo = opera_corrente['titolo'] if opera_corrente else ""
        v_testo = opera_corrente['contenuto'] if opera_corrente else ""
        v_cat = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"

        col_t, col_c = st.columns([2, 1])
        with col_t:
            titolo = st.text_input("Titolo dell'Opera", value=v_titolo)
        with col_c:
            cats = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
            idx = cats.index(v_cat) if v_cat in cats else 0
            categoria = st.selectbox("Categoria", cats, index=idx)

        contenuto = st.text_area("Versi e Pensieri", value=v_testo, height=400)

        st.write("---")
        b1, b2, b3, b4 = st.columns([1, 1, 1, 1])

        with b1:
            if st.button("💾 Salva nel Diario", key="btn_salva"):
                if titolo:
                    dati = {"titolo": titolo, "contenuto": contenuto, "categoria": categoria, "autore_email": nome_poeta}
                    if opera_corrente:
                        supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                    else:
                        supabase.table("Opere").insert(dati).execute()
                    st.success("Versi custoditi con cura.")
                    st.rerun()
                else:
                    st.warning("Un'opera ha bisogno di un titolo.")

        with b2:
            if st.button("🖨️ Stampa Foglio", key="btn_stampa"):
                st.markdown("<script>window.print();</script>", unsafe_allow_html=True)

        with b3:
            if opera_corrente:
                if st.button("🗑️ Brucia Opera", key="btn_cancella"):
                    supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                    st.rerun()
    else:
        st.warning("Identificati nella Home per accedere allo Scrittoio.")