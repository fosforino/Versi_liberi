import streamlit as st
from supabase import create_client

def show():
    # --- NUOVO STILE STRAVOLTO PER LO SCRITTOIO ---
    st.markdown("""
        <style>
        /* SFONDO VERDINO SMERALDO DELICATO */
        .stApp {
            background-color: #e0f2f1 !important; /* Un verde acqua chiarissimo e fresco */
            background-image: none !important; /* Togliamo la vecchia pergamena */
        }

        /* TITOLO TITOLO */
        h1 {
            color: #004d40 !important; /* Verde pino scuro per contrasto */
            font-family: 'Playfair Display', serif;
            text-align: center;
        }

        /* AREA DI TESTO - Foglio di carta bianca pulita */
        textarea, input {
            background-color: #ffffff !important;
            border: 2px solid #b2dfdb !important; /* Bordo verde chiarissimo */
            border-radius: 8px !important;
            color: #004d40 !important;
            font-size: 1.2rem !important;
        }

        /* --- I BOTTONI TRIDIMENSIONALI CHE CAMBIANO COLORE --- */
        
        /* Stile base per tutti i bottoni dello scrittoio */
        div.stButton > button {
            border-radius: 12px !important;
            border: none !important;
            font-family: 'Playfair Display', serif !important;
            font-weight: bold !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.1s ease-in-out !important; /* Transizione veloce per il clic */
            
            /* L'effetto 3D: un'ombra solida e scura in basso */
            box-shadow: 0 6px 0 rgba(0,0,0,0.2) !important;
            position: relative;
            top: 0;
        }

        /* 1. BOTTONE SALVA (Verde) */
        div.stButton > button[key="btn_salva"] {
            background-color: #4db6ac !important; /* Verde smeraldo medio */
            color: white !important;
        }
        /* Quando ci passi sopra */
        div.stButton > button[key="btn_salva"]:hover {
            background-color: #80cbc4 !important; /* Si schiarisce */
        }
        /* QUANDO LO CLICCHI: Il cambio colore e movimento */
        div.stButton > button[key="btn_salva"]:active {
            background-color: #00796b !important; /* Diventa verde scuro e saturo */
            box-shadow: 0 2px 0 rgba(0,0,0,0.2) !important; /* L'ombra si riduce */
            top: 4px; /* Il bottone si abbassa */
        }

        /* 2. BOTTONE STAMPA (Blu) */
        div.stButton > button[key="btn_stampa"] {
            background-color: #4fc3f7 !important; /* Blu cielo */
            color: white !important;
        }
        div.stButton > button[key="btn_stampa"]:hover {
            background-color: #81d4fa !important;
        }
        div.stButton > button[key="btn_stampa"]:active {
            background-color: #0277bd !important; /* Diventa blu scuro */
            box-shadow: 0 2px 0 rgba(0,0,0,0.2) !important;
            top: 4px;
        }

        /* 3. BOTTONE BRUCIA/ELIMINA (Rosso) */
        div.stButton > button[key="btn_cancella"] {
            background-color: #ef5350 !important; /* Rosso corallo */
            color: white !important;
        }
        div.stButton > button[key="btn_cancella"]:hover {
            background-color: #e57373 !important;
        }
        div.stButton > button[key="btn_cancella"]:active {
            background-color: #c62828 !important; /* Diventa rosso scuro */
            box-shadow: 0 2px 0 rgba(0,0,0,0.2) !important;
            top: 4px;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- LOGICA SUPABASE (Invariata) ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    if "utente" in st.session_state:
        nome_poeta = st.session_state.utente
        st.markdown(f"<h1>✒️ Lo Scrittoio di {nome_poeta}</h1>", unsafe_allow_html=True)

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
                    st.success("Versi custoditi.")
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