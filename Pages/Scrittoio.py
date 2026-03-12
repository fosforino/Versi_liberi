import streamlit as st
from supabase import create_client

def show():
    # --- 1. Estetica (Sfondo crema e font Serif) ---
    st.markdown("""
        <style>
        .stApp {
            background-color: #f5f5dc;
        }
        h1, h2, h3, p, label {
            font-family: 'Georgia', serif;
            color: #2c3e50;
        }
        .stButton>button {
            border-radius: 20px;
            font-family: 'Georgia', serif;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- 2. Connessione a Supabase ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    # --- 3. Controllo Sessione Utente ---
    if "user" in st.session_state:
        user_id = st.session_state.user.id
        user_email = st.session_state.user.email

        st.title("✒️ Lo Scrittoio")
        st.write(f"*Benvenuto, {user_email}. Lascia che le tue parole trovino dimora.*")

        # --- SIDEBAR: Archivio sulla tabella 'Opere' ---
        st.sidebar.header("Il tuo Archivio")
        try:
            res = supabase.table("Opere").select("*").eq("user_id", user_id).order("creato_il", desc=True).execute()
            opere = res.data
        except Exception:
            opere = []

        opzioni_archivio = ["Nuova Opera"] + [o['titolo'] for o in opere]
        scelta = st.sidebar.selectbox("Carica un'opera:", opzioni_archivio)

        opera_corrente = next((o for o in opere if o['titolo'] == scelta), None)
        
        # Variabili pre-compilate
        val_titolo = opera_corrente['titolo'] if opera_corrente else ""
        val_contenuto = opera_corrente['contenuto'] if opera_corrente else ""
        val_cat = opera_corrente.get('categoria', "Poesia") if opera_corrente else "Poesia"

        # --- INTERFACCIA PRINCIPALE ---
        col1, col2 = st.columns([2, 1])
        with col1:
            titolo = st.text_input("Titolo dell'Opera", value=val_titolo)
        with col2:
            lista_categories = ["Poesia", "Romanzo", "Filastrocca", "Narrazione", "Opera Teatrale", "Canzone"]
            idx_cat = lista_categories.index(val_cat) if val_cat in lista_categories else 0
            categoria = st.selectbox("Categoria", lista_categories, index=idx_cat)

        contenuto = st.text_area("Versi o Prosa", value=val_contenuto, height=400)

        # --- TASTI AZIONE ---
        col_salva, col_canc, col_stampa = st.columns(3)

        with col_salva:
            if st.button("💾 Salva nel Registro"):
                dati = {
                    "user_id": user_id,
                    "titolo": titolo,
                    "contenuto": contenuto,
                    "categoria": categoria,
                    "autore_email": user_email
                }
                
                if opera_corrente: # Aggiorna
                    supabase.table("Opere").update(dati).eq("id", opera_corrente['id']).execute()
                    st.success("L'opera è stata aggiornata.")
                else: # Inserisci nuova
                    supabase.table("Opere").insert(dati).execute()
                    st.success("L'opera è stata salvata con successo.")
                st.rerun()

        with col_canc:
            if opera_corrente:
                if st.button("🗑️ Elimina", type="secondary"):
                    supabase.table("Opere").delete().eq("id", opera_corrente['id']).execute()
                    st.rerun()

        with col_stampa:
            if titolo and contenuto:
                testo_stampa = f"{titolo}\n\nCategoria: {categoria}\n\n{contenuto}"
                st.download_button(
                    label="🖨️ Scarica TXT",
                    data=testo_stampa,
                    file_name=f"{titolo}.txt",
                    mime="text/plain"
                )
    else:
        st.warning("Accedi dalla Home per iniziare a scrivere.")

# Avvio automatico per test locale
if __name__ == "__main__":
    show()