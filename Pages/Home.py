import streamlit as st

def apply_aesthetic_style():
    """Applica l'estetica coerente 'Parchment & Ink' alla Home."""
    st.markdown(
        """
        <style>
        /* Sfondo generale color crema */
        .stApp {
            background-color: #fdf5e6;
            color: #2c2c2c;
        }

        /* Titolo e Sottotitolo */
        .poetic-title-home { 
            font-family: 'Playfair Display', serif; 
            font-size: 3.5rem; 
            color: #4b3621; 
            text-align: center;
            margin-top: -20px;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.05);
        }
        .home-subtitle {
            font-family: 'EB Garamond', serif;
            font-style: italic;
            font-size: 1.5rem;
            text-align: center;
            color: #8c6d46;
            margin-bottom: 40px;
        }

        /* Box delle funzionalità (Effetto carta pregiata) */
        .feature-box {
            background-color: #fffaf0;
            padding: 25px;
            border-radius: 4px;
            border-left: 4px solid #d2b48c;
            border-right: 1px solid #eee;
            border-bottom: 1px solid #eee;
            margin-bottom: 20px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.03);
        }
        
        .feature-box strong {
            color: #4b3621;
            font-family: 'Playfair Display', serif;
            font-size: 1.2rem;
        }

        /* Colonna Regole (Sidebar-like interna) */
        .rules-card {
            background-color: #f4ece0;
            padding: 20px;
            border-radius: 8px;
            border: 1px dashed #8c6d46;
            font-family: 'EB Garamond', serif;
        }

        /* Divider personalizzato */
        hr {
            border: 0;
            height: 1px;
            background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(75, 54, 33, 0.4), rgba(0, 0, 0, 0));
            margin: 40px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def show():
    apply_aesthetic_style()

    # Intestazione
    st.markdown("<h1 class='poetic-title-home'>Benvenuto in Poeticamente ✒️</h1>", unsafe_allow_html=True)
    st.markdown("<p class='home-subtitle'>La tua dimora per l'arte del verso</p>", unsafe_allow_html=True)
    
    # Layout a due colonne
    col1, col2 = st.columns([2, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div style='font-family: "EB Garamond", serif; font-size: 1.2rem; line-height: 1.6;'>
        Poeticamente è uno spazio sacro dedicato a chi trasforma il silenzio in rime. 
        Qui, ogni parola ha un peso e ogni autore un volto, per proteggere la bellezza 
        e l'integrità del tuo sentire.
        <br><br>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='feature-box'>
            <strong>🖋️ Lo Scrittoio:</strong>
            <p>Il tuo spazio privato di creazione. Componi in tranquillità, con la cura di chi stila un manoscritto prezioso.</p>
        </div>
        <div class='feature-box'>
            <strong>📖 La Bacheca:</strong>
            <p>Affiggi i tuoi versi al cuore del mondo. Leggi e lasciati ispirare dalle opere della nostra comunità.</p>
        </div>
        <div class='feature-box'>
            <strong>📜 L'Archivio:</strong>
            <p>Il registro delle tue pubblicazioni, custodito sotto il tuo pseudonimo univoco.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='rules-card'>
            <h4 style='text-align: center; margin-top: 0; color: #4b3621;'>Il Codice del Poeta</h4>
            <ol>
                <li><strong>Identità:</strong> Lo pseudonimo è il tuo vessillo; sceglilo con cura.</li>
                <li><strong>Decoro:</strong> La poesia eleva l'animo. Evitiamo linguaggi impropri.</li>
                <li><strong>Legame:</strong> Ogni verso appartiene al suo autore per sempre.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Messaggio di stato elegante
    if st.session_state.get('utente'):
        st.markdown(
            f"""
            <div style='text-align: center; padding: 15px; border-radius: 50px; background-color: rgba(76, 175, 80, 0.1); border: 1px solid #4CAF50;'>
                Bentornato, <strong>{st.session_state.utente}</strong>. Il tuo calamaio è pronto nello Scrittoio.
            </div>
            """, 
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style='text-align: center; padding: 15px; border-radius: 50px; background-color: rgba(255, 152, 0, 0.1); border: 1px solid #FF9800;'>
                Posa il tuo mantello e identifica il tuo profilo nella barra laterale per iniziare a scrivere.
            </div>
            """, 
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    show()