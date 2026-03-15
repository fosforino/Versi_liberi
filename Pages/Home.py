import streamlit as st
import os
import base64

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

def apply_aesthetic_style():
    """Applica l'estetica 'Parchment & Ink' con icona sfocata."""
    path_icona = "Poeticamente.png"
    img_base64 = get_base64_image(path_icona)
    img_html = ""
    
    if img_base64:
        # Filigrana sfocata specifica per la Home
        img_html = f"""
        <img src="data:image/png;base64,{img_base64}" class="bg-watermark-home">
        """

    st.markdown(
        f"""
        <style>
        /* Sfondo Pergamena (Ereditato da app.py, qui rifiniamo i dettagli) */
        .stApp {{
            background-color: #fdf5e6;
            color: #3e2723;
        }}

        /* ICONA FILIGRANA */
        .bg-watermark-home {{
            position: fixed;
            top: 55%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 65vw;
            opacity: 0.06;
            filter: blur(10px);
            z-index: -1;
            pointer-events: none;
        }}

        /* Titolo e Sottotitolo Antichi */
        .poetic-title-home {{ 
            font-family: 'Playfair Display', serif; 
            font-size: 3.8rem; 
            color: #3e2723; 
            text-align: center;
            margin-top: -30px;
            letter-spacing: 1px;
        }}
        
        .home-subtitle {{
            font-family: 'EB Garamond', serif;
            font-style: italic;
            font-size: 1.6rem;
            text-align: center;
            color: #795548;
            margin-bottom: 40px;
        }}

        /* Box Funzionalità (Effetto Carta Pregiata) */
        .feature-box {{
            background-color: rgba(255, 250, 240, 0.6);
            padding: 22px;
            border-radius: 4px;
            border-left: 3px solid #c19a6b;
            margin-bottom: 15px;
            box-shadow: 1px 1px 5px rgba(0,0,0,0.02);
            color: #3e2723;
        }}
        
        .feature-box strong {{
            color: #3e2723;
            font-family: 'Playfair Display', serif;
            font-size: 1.3rem;
        }}

        /* Pergamena delle Regole */
        .rules-card {{
            background-color: #f4ece0;
            padding: 20px;
            border-radius: 2px;
            border: 1px solid #d2b48c;
            font-family: 'EB Garamond', serif;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
        }}

        /* Messaggi di Stato (Sostituito il verde smeraldo con tonalità terra) */
        .status-msg {{
            text-align: center; 
            padding: 15px; 
            border-radius: 4px; 
            background-color: rgba(193, 154, 107, 0.15); 
            border: 1px solid #c19a6b;
            color: #3e2723;
            font-style: italic;
        }}
        </style>
        {img_html}
        """,
        unsafe_allow_html=True
    )

def show():
    apply_aesthetic_style()

    # Intestazione
    st.markdown("<h1 class='poetic-title-home'>Poeticamente ✒️</h1>", unsafe_allow_html=True)
    st.markdown("<p class='home-subtitle'>Dimora sacra per l'arte del verso</p>", unsafe_allow_html=True)
    
    # Layout a due colonne
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style='font-family: "EB Garamond", serif; font-size: 1.3rem; line-height: 1.7; text-align: justify;'>
        Poeticamente è uno spazio dedicato a chi trasforma il silenzio in rime. 
        Qui, ogni parola ha un peso e ogni autore un volto, per proteggere la bellezza 
        del tuo sentire. Ogni verso affidato a queste pagine diventa parte di un'antologia senza tempo.
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-box'>
            <strong>🖋️ Lo Scrittoio</strong>
            <p>Il tuo spazio privato. Componi in tranquillità, con la cura di chi stila un manoscritto prezioso.</p>
        </div>
        <div class='feature-box'>
            <strong>📖 La Bacheca</strong>
            <p>Affiggi i tuoi versi al cuore del mondo. Leggi e lasciati ispirare dalla comunità.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='rules-card'>
            <h4 style='text-align: center; margin-top: 0; color: #3e2723;'>Il Codice del Poeta</h4>
            <ul style='list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 10px;'>📜 <b>Identità:</b> Il tuo pseudonimo è il tuo vessillo.</li>
                <li style='margin-bottom: 10px;'>✒️ <b>Decoro:</b> La poesia eleva l'animo e il linguaggio.</li>
                <li style='margin-bottom: 10px;'>🔒 <b>Legame:</b> Ogni verso appartiene al suo autore.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Messaggio di stato (niente più verde smeraldo acceso)
    if st.session_state.get('utente'):
        st.markdown(
            f"""
            <div class='status-msg'>
                Bentornato, <strong>{st.session_state.utente}</strong>. Il tuo calamaio ti attende nello Scrittoio.
            </div>
            """, 
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    show()