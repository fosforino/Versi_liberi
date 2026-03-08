import streamlit as st
from supabase import create_client, Client

# --- CONNESSIONE SUPABASE ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

def apply_aesthetic_style():
    """Applica lo stile pergamena e l'estetica vintage alla pagina."""
    st.markdown(
        """
        <style>
        /* Sfondo dell'intera applicazione color crema/pergamena */
        .stApp {
            background-color: #fdf5e6;
            color: #2c2c2c;
        }

        /* Font Serif per titoli e testi eleganti */
        h1, h2, h3, h4 {
            font-family: 'Playfair Display', serif;
            color: #4b3621; /* Un marrone testa di moro per l'inchiostro */
        }

        /* Stile per i contenitori delle opere */
        .stContainer {
            background-color: #fffaf0;
            padding: 20px;
            border-radius: 5px;
            border: 1px solid #d2b48c;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        /* Input e bottoni */
        .stButton>button {
            border-radius: 20px;
            border: 1px solid #4b3621;
            background-color: transparent;
            color: #4b3621;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #4b3621;
            color: #fdf5e6;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show():
    apply_aesthetic_style()
    
    st.markdown("<h1 style='text-align: center;'>Lo Scrittoio di Poeticamente ✒️</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; color: #6b4a3a;'>Il luogo dove i pensieri prendono forma di verso.</p>", unsafe_allow_html=True)
    
    # --- CREAZIONE OPERA ---
    with st.expander("📝 Componi una nuova Opera", expanded=True):
        titolo = st.text_input("Titolo dell'Opera:", key="new_titolo")
        testo = st.text_area("Versi:", height=200, key="new_testo")
        url_immagine = st.text_input("URL Immagine Ispirazionale (Opzionale):")
        
        if st.button("Pubblica su Poeticamente"):
            if titolo and testo:
                data = {
                    "autore": st.session_state.utente,
                    "titolo": titolo,
                    "testo": testo,
                    "immagine_url": url_immagine if url_immagine else None
                }
                try:
                    supabase.table("opere").insert(data).execute()
                    st.success("L'opera è stata impressa nel database.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Errore nel salvataggio: {e}")
            else:
                st.warning("Titolo e Testo sono il cuore dell'opera. Non possono mancare.")

    st.write("---")
    st.markdown("### 📜 Le Tue Opere")

    # --- RECUPERO DATI ---
    response = supabase.table("opere").select("*").eq("autore", st.session_state.utente).order("created_at", desc=True).execute()
    opere = response.data

    if not opere:
        st.info("Il tuo registro è ancora bianco. Comincia a scrivere!")
    else:
        for opera in opere:
            with st.container():
                col_testo, col_azioni = st.columns([3, 1])
                
                with col_testo:
                    st.markdown(f"<h4 style='margin-bottom: 0;'>{opera['titolo']}</h4>", unsafe_allow_html=True)
                    # Usiamo markdown con interruzioni di riga per preservare la struttura dei versi
                    st.markdown(f"<div style='white-space: pre-wrap; font-family: serif; padding: 10px 0;'>{opera['testo']}</div>", unsafe_allow_html=True)
                    
                    if opera.get('immagine_url'):
                        st.image(opera['immagine_url'], width=300)
                
                with col_azioni:
                    if st.button("Modifica ✏️", key=f"btn_edit_{opera['id']}"):
                        st.session_state[f"editing_{opera['id']}"] = True
                    
                    if st.button("Elimina 🗑️", key=f"btn_del_{opera['id']}"):
                        supabase.table("opere").delete().eq("id", opera['id']).execute()
                        st.rerun()

                # --- FORM DI MODIFICA INLINE ---
                if st.session_state.get(f"editing_{opera['id']}", False):
                    with st.form(key=f"edit_form_{opera['id']}"):
                        edit_titolo = st.text_input("Modifica Titolo", value=opera['titolo'])
                        edit_testo = st.text_area("Modifica Versi", value=opera['testo'], height=150)
                        edit_img = st.text_input("Modifica URL Immagine", value=opera.get('immagine_url', ''))
                        
                        c1, c2 = st.columns(2)
                        if c1.form_submit_button("Salva"):
                            supabase.table("opere").update({
                                "titolo": edit_titolo,
                                "testo": edit_testo,
                                "immagine_url": edit_img if edit_img else None
                            }).eq("id", opera['id']).execute()
                            st.session_state[f"editing_{opera['id']}"] = False
                            st.rerun()
                        
                        if c2.form_submit_button("Annulla"):
                            st.session_state[f"editing_{opera['id']}"] = False
                            st.rerun()
                
                st.markdown("<hr style='border: 0.5px solid #d2b48c; opacity: 0.3;'>", unsafe_allow_html=True)