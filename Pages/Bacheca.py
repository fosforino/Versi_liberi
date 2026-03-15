import streamlit as st
from supabase import create_client
import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_aesthetic_style():
    """Applica l'estetica vintage e la filigrana alla Bacheca."""
    path_icona = "Poeticamente.png"
    img_base64 = get_base64_image(path_icona)
    img_html = f'<img src="data:image/png;base64,{img_base64}" class="bg-watermark-bacheca">' if img_base64 else ""

    st.markdown(f"""
        <style>
        /* Sfondo Pergamena */
        .stApp {{
            background-color: #fdf5e6;
            background-image: url("https://www.transparenttextures.com/patterns/handmade-paper.png");
            color: #3e2723;
        }}

        /* ICONA FILIGRANA */
        .bg-watermark-bacheca {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 60vw;
            opacity: 0.05;
            filter: blur(10px);
            z-index: -1;
            pointer-events: none;
        }}

        /* Contenitore Poesia (Effetto foglio pregiato) */
        .poesia-card {{
            background-color: rgba(255, 250, 240, 0.8);
            padding: 35px;
            border-radius: 2px;
            border-left: 4px solid #c19a6b;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 50px;
            transition: all 0.3s ease;
        }}
        
        .poesia-card:hover {{
            transform: scale(1.01);
            background-color: rgba(255, 255, 255, 0.9);
        }}

        .titolo-poesia {{
            font-family: 'Playfair Display', serif;
            color: #3e2723;
            font-size: 2rem;
            margin-bottom: 10px;
            text-align: left;
        }}

        .versi-testo {{
            font-family: 'EB Garamond', serif;
            font-size: 1.3rem;
            line-height: 1.6;
            white-space: pre-wrap;
            color: #2c2c2c;
            margin: 25px 0;
        }}

        .firma-autore {{
            font-family: 'Playfair Display', serif;
            font-style: italic;
            text-align: right;
            color: #795548;
            font-size: 1rem;
            border-top: 1px solid rgba(193, 154, 107, 0.3);
            padding-top: 15px;
        }}
        </style>
        {img_html}
        """, unsafe_allow_html=True)

def show():
    apply_aesthetic_style()
    
    st.markdown("<h1 style='font-size: 3.5rem;'>Bacheca Poetica</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; font-size: 1.2rem; color: #795548; margin-bottom: 60px;'>Le voci dei poeti si rincorrono tra i fogli del tempo.</p>", unsafe_allow_html=True)
    
    # --- CONNESSIONE SUPABASE ---
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)

    try:
        # Recupero ultime 20 opere (usando i nomi colonne corretti dello Scrittoio)
        res = supabase.table("Opere").select("*").order("creato_il", desc=True).limit(20).execute()
        poemi = res.data if res.data else []

        if not poemi:
            st.info("La bacheca è ancora bianca. Sii il primo a lasciare un'impronta!")
        
        # Layout centrato per le poesie
        col_m_1, col_m_2, col_m_3 = st.columns([0.2, 1, 0.2])
        
        with col_m_2:
            for p in poemi:
                st.markdown(
                    f"""
                    <div class="poesia-card">
                        <div class="titolo-poesia">{p['titolo']}</div>
                        <div style='color: #c19a6b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;'>{p.get('categoria', 'Poesia')}</div>
                        <div class="versi-testo">{p['contenuto']}</div>
                        <div class="firma-autore">Affisso dal Poeta: {p['autore_email']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
    except Exception as e:
        st.error(f"Il calamaio della bacheca è momentaneamente asciutto.")

if __name__ == "__main__":
    show()