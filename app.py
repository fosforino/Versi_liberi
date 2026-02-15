import streamlit as st
import requests
import json
import re
import base64
from fpdf import FPDF
from datetime import datetime

# --- CONFIGURAZIONE DATABASE (SUPABASE) ---
URL_SUPABASE = "https://eeavavlfgeeusijiljfw.supabase.co"
KEY_SUPABASE = ""

# --- LOGICA BACKEND ---

def invia_opera(record):
    endpoint = f"{URL_SUPABASE}/rest/v1/Poesie"
    headers = {"apikey": KEY_SUPABASE, "Authorization": f"Bearer {KEY_SUPABASE}", "Content-Type": "application/json"}
    return requests.post(endpoint, headers=headers, data=json.dumps(record))

def verifica_limite_demo(autore_nome):
    endpoint = f"{URL_SUPABASE}/rest/v1/Poesie?select=id&autore=eq.{autore_nome}"
    headers = {"apikey": KEY_SUPABASE, "Authorization": f"Bearer {KEY_SUPABASE}"}
    try:
        res = requests.get(endpoint, headers=headers)
        return len(res.json()) if res.status_code == 200 else 0
    except: return 0

def esporta_pdf(titolo, testo, autore):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", 'B', 22)
    pdf.cell(0, 20, titolo.upper(), ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Times", 'I', 14)
    pdf.multi_cell(0, 10, testo, align='C')
    return pdf.output(dest="S").encode("latin-1", "replace")

# --- INIZIALIZZAZIONE SESSIONE (Risolve il blocco dei tasti) ---
if 'is_pro' not in st.session_state:
    st.session_state.is_pro = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = "Poeta_Anonimo"

# --- INTERFACCIA E CSS ---
st.set_page_config(page_title="Versi Liberi", page_icon="✒️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display&family=EB+Garamond&display=swap');
    
    .stApp { background-color: #f5eedc; background-image: url("https://www.transparenttextures.com/patterns/natural-paper.png"); }
    [data-testid="stSidebar"] { background-color: #1a0f08 !important; }
    [data-testid="stSidebar"] * { color: #d4af37 !important; }
    
    .demo-banner { 
        background-color: #1a0f08; 
        color: #d4af37; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center; 
        margin-bottom: 25px;
        border: 1px solid #d4af37;
    }
    
    .plan-card { 
        background: white; 
        padding: 40px; 
        border-radius: 20px; 
        text-align: center; 
        box-shadow: 10px 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #e5d3b3;
    }
    
    .stMetric { background: rgba(255,255,255,0.5); padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVIGAZIONE SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align:center;'>Versi Liberi</h1>", unsafe_allow_html=True)
    scelta = st.radio("STANZA:", ["Home", "Scrittoio", "Bacheca", "Piani"])
    st.markdown("---")
    st.write("📱 Social: WhatsApp | Instagram")

# --- LOGICA PAGINE ---

if scelta == "Scrittoio":
    st.markdown("<h1 style='font-family:Playfair Display;'>✒️ Lo Scrittoio</h1>", unsafe_allow_html=True)
    
    # Calcolo demo dinamico
    n_salvati = verifica_limite_demo(st.session_state.user_name)
    
    if not st.session_state.is_pro:
        st.markdown(f'<div class="demo-banner">✨ MODALITÀ DEMO: {n_salvati} di 3 salvataggi usati</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="demo-banner" style="background:#d4af37; color:#1a0f08;">💎 PROFILO PRO ATTIVO</div>', unsafe_allow_html=True)

    titolo = st.text_input("Titolo dell'opera", placeholder="Inserisci il titolo...")
    testo = st.text_area("Inizia a scrivere...", height=300)

    # Metriche
    c1, c2, c3 = st.columns(3)
    c1.metric("Parole", len(testo.split()))
    c2.metric("Versi", len([r for r in testo.split('\n') if r.strip()]))
    c3.metric("Sillabe", sum(1 for c in testo if c.lower() in "aeiouàèéìòù"))

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("💾 SALVA"):
            if not st.session_state.is_pro and n_salvati >= 3:
                st.error("Limite demo raggiunto. Scegli un piano Pro per continuare.")
            elif titolo and testo:
                invia_opera({"titolo": titolo, "versi": testo, "autore": st.session_state.user_name})
                st.success("Opera salvata con successo!")
                st.rerun()

    with col_btn2:
        if titolo and testo:
            pdf_bytes = esporta_pdf(titolo, testo, st.session_state.user_name)
            b64 = base64.b64encode(pdf_bytes).decode()
            st.markdown(f'<a href="data:application/pdf;base64,{b64}" download="{titolo}.pdf" style="text-decoration:none; background:#7d1d1d; color:white; padding:10px; border-radius:5px; display:block; text-align:center;">📄 SCARICA PDF</a>', unsafe_allow_html=True)

elif scelta == "Piani":
    st.markdown("<h1 style='text-align:center; font-family:Playfair Display;'>ABBONAMENTI</h1>", unsafe_allow_html=True)
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="plan-card"><h2>Mensile</h2><br><h1>3,99€</h1><p>Versi Illimitati</p></div>', unsafe_allow_html=True)
        if st.button("SCEGLI MENSILE", key="m"):
            st.session_state.is_pro = True
            st.success("Sei ora un utente PRO! Limiti rimossi.")
            st.balloons()
            
    with p2:
        st.markdown('<div class="plan-card"><h2>Annuale</h2><br><h1>39,90€</h1><p>Include AI Inspirer</p></div>', unsafe_allow_html=True)
        if st.button("SCEGLI ANNUALE", key="a"):
            st.session_state.is_pro = True
            st.success("Sei ora un utente PRO Annuale! IA sbloccata.")
            st.balloons()

elif scelta == "Home":
    st.markdown("<h1 style='text-align:center;'>Versi Liberi</h1>", unsafe_allow_html=True)
    st.write("Benvenuto nel tuo spazio creativo digitale.")