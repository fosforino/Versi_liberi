import streamlit as st
import random
import time
from supabase import create_client, Client

# --- 1. CONNESSIONE DATABASE ---
# Assicurati di avere SUPABASE_URL e SUPABASE_KEY nei tuoi Secrets di Streamlit
URL_SUPABASE = st.secrets["SUPABASE_URL"]
KEY_SUPABASE = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(URL_SUPABASE, KEY_SUPABASE)

# --- 2. CONFIGURAZIONE PAGINA ED ESTETICA ---
st.set_page_config(page_title="Poeticamente", page_icon="✍️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&family=EB+Garamond&display=swap');
    .stApp { background-color: #f5eedc; background-image: url("https://www.transparenttextures.com/patterns/natural-paper.png"); }
    [data-testid="stSidebar"] { background-color: #f0f2f6 !important; }
    .poesia-card { 
        background: white; padding: 25px; border-radius: 12px; border-left: 6px solid #d4af37; 
        margin-bottom: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); font-family: 'EB Garamond', serif;
    }
    .id-tag { background: #1a0f08; color: #d4af37; padding: 3px 8px; border-radius: 4px; font-family: monospace; font-size: 0.8em; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGICA DI ACCESSO ---
if "user_email" not in st.session_state:
    st.markdown("<h1 style='text-align:center; font-family:Playfair Display;'>Poeticamente</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        email = st.text_input("Inserisci la tua Email")
        codice = st.text_input("Codice (123456)", type="password")
        if st.button("Entra nella tua Stanza"):
            if email and codice == "123456":
                st.session_state.user_email = email
                st.rerun()
    st.stop()

user_mail = st.session_state.user_email

# --- 4. NAVIGAZIONE ---
with st.sidebar:
    st.markdown(f"### Poeticamente")
    st.write(f"Poeta: **{user_mail}**")
    st.divider()
    scelta = st.radio("Spostati in:", ["Lo Scrittoio", "La Bacheca Pubblica", "Gestisci Opere"])
    st.divider()
    if st.button("Esci"):
        del st.session_state.user_email
        st.rerun()

# --- 5. FUNZIONI DATABASE ---
def carica_opere(solo_mie=False):
    query = supabase.table("poesie").select("*")
    if solo_mie:
        query = query.eq("autore_email", user_mail)
    return query.execute().data

# --- SEZIONE: LO SCRITTOIO ---
if scelta == "Lo Scrittoio":
    st.subheader("✒️ Crea o Modifica")
    
    # Controllo se stiamo modificando
    id_mod = st.session_state.get("id_in_modifica", None)
    val_t, val_c, val_cat = "", "", "Poesia"
    
    if id_mod:
        res = supabase.table("poesie").select("*").eq("id", id_mod).execute()
        if res.data:
            val_t, val_c, val_cat = res.data[0]['titolo'], res.data[0]['contenuto'], res.data[0]['categoria']
            st.warning(f"Modifica in corso: {id_mod}")

    titolo = st.text_input("Titolo", value=val_t)
    cat = st.selectbox("Tipo di opera", ["Poesia", "Romanzo", "Racconto", "Video-Canzone"], index=0)
    testo = st.text_area("Scrivi qui...", value=val_c, height=300)
    
    if st.button("💾 SALVA SU POETICAMENTE"):
        if titolo and testo:
            nuovo_id = id_mod if id_mod else f"ID-{random.randint(1000, 9999)}"
            dati = {
                "id": nuovo_id,
                "titolo": titolo,
                "contenuto": testo,
                "categoria": cat,
                "autore_email": user_mail
            }
            supabase.table("poesie").upsert(dati).execute()
            st.success("Salvato correttamente nel database!")
            if "id_in_modifica" in st.session_state: del st.session_state.id_in_modifica
            time.sleep(1)
            st.rerun()

# --- SEZIONE: GESTISCI OPERE ---
elif scelta == "Gestisci Opere":
    st.subheader("🛠️ La tua Stanza Privata")
    mie = carica_opere(solo_mie=True)
    if not mie:
        st.info("Non hai ancora creato nulla.")
    else:
        for o in mie:
            with st.expander(f"{o['titolo']} ({o['categoria']})"):
                st.write(o['contenuto'])
                c1, c2, c3 = st.columns(3)
                if c1.button("📝 Modifica", key=f"ed_{o['id']}"):
                    st.session_state.id_in_modifica = o['id']
                    st.info("Vai allo Scrittoio per modificare!")
                if c2.button("🗑️ Elimina", key=f"del_{o['id']}"):
                    supabase.table("poesie").delete().eq("id", o['id']).execute()
                    st.error("Eliminato!")
                    st.rerun()

# --- SEZIONE: BACHECA ---
elif scelta == "La Bacheca Pubblica":
    st.subheader("📜 Opere della Community")
    tutte = carica_opere()
    for o in tutte:
        st.markdown(f"""
        <div class="poesia-card">
            <div style="display:flex; justify-content:space-between;">
                <span class="id-tag">{o['id']}</span>
                <small>{o['categoria']}</small>
            </div>
            <h3>{o['titolo']}</h3>
            <p style="white-space: pre-wrap;">{o['contenuto']}</p>
            <hr>
            <small>Scritto da: {o['autore_email']} | ❤️ {o.get('likes', 0)}</small>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"Apprezza ❤️", key=f"lk_{o['id']}"):
            supabase.table("poesie").update({"likes": o.get('likes', 0) + 1}).eq("id", o['id']).execute()
            st.rerun()