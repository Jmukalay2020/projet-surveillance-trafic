import streamlit as st  # Bibliothèque pour créer des interfaces web interactives
import requests
import pandas as pd
import os
from PIL import Image

# --- Configuration de la page et du menu latéral ---
st.set_page_config(page_title="Surveillance Trafic Kolwezi", page_icon="🚦", layout="centered")
st.sidebar.image("https://img.icons8.com/color/96/traffic-jam.png", width=80)
st.sidebar.title("Menu")
st.sidebar.markdown("""
- [Documentation](https://github.com/ISICOM-TECH)
- [Contact](mailto:isicomtech@gmail.com)
- [À propos](#)
""")
st.sidebar.markdown("---")
st.sidebar.info("Projet ISICOM TECH - 2025")

# --- Style CSS personnalisé ---
st.markdown('''
    <style>
    .main {background-color: #f5f7fa;}
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: #800000;
        text-align: center;
        margin-bottom: 0.2em;
        letter-spacing: 2px;
    }
    .subtitle {
        color: #0072C6;
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 1em;
    }
    .stButton>button {background-color: #0072C6; color: white; font-weight: bold;}
    .stDownloadButton>button {background-color: #00B050; color: white; font-weight: bold;}
    .result-box {
        background: #fff3cd;
        border-radius: 8px;
        padding: 1em;
        margin-top: 1em;
        border: 1px solid #ffeeba;
    }
    .footer {text-align: center; color: #888; font-size: 0.9em; margin-top: 2em;}
    </style>
''', unsafe_allow_html=True)

# --- En-tête ---
st.markdown('<div class="title">🚦 Surveillance du Trafic Routier à Kolwezi 🚦</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Détection automatique des embouteillages et analyse du trafic</div>', unsafe_allow_html=True)

# --- Upload vidéo/image ---
st.header('📊 Tableau de bord du trafic')
if os.path.exists('resultats_api.csv'):
    csv_path_abs = os.path.abspath('resultats_api.csv')
    st.info(f"Chemin du CSV utilisé : {csv_path_abs}")
    try:
        with open(csv_path_abs, 'r', encoding='utf-8') as f:
            csv_content = f.read()
        st.code(csv_content, language='csv')
        df_dash = pd.read_csv(csv_path_abs)
        st.info(f"Aperçu du CSV :\n{df_dash.head().to_string(index=False)}")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du CSV : {e}")
        df_dash = pd.DataFrame({'count': []})
else:
    df_dash = pd.DataFrame({'count': []})
with st.container():
    dash1, dash2, dash3, dash4 = st.columns(4)
    dash1.metric("Frames analysées", str(len(df_dash)) if not df_dash.empty else "-")
    dash2.metric("Total véhicules", str(int(df_dash['count'].sum())) if not df_dash.empty and 'count' in df_dash.columns else "-")
    dash3.metric("Véhicules max/frame", str(int(df_dash['count'].max())) if not df_dash.empty and 'count' in df_dash.columns else "-")
    dash4.metric("Véhicules min/frame", str(int(df_dash['count'].min())) if not df_dash.empty and 'count' in df_dash.columns else "-")
    st.line_chart(df_dash['count'] if not df_dash.empty and 'count' in df_dash.columns else pd.Series(dtype=int))
    st.bar_chart(df_dash['count'].value_counts().sort_index() if not df_dash.empty and 'count' in df_dash.columns else pd.Series(dtype=int))
    # --- Analyse congestion et conseils ---
    if not df_dash.empty and 'count' in df_dash.columns:
        st.markdown('---')
        st.header('🚦 Analyse de congestion et conseils')
        congestion_frames = 0
        seuil_congestion = df_dash['count'].quantile(0.9)
        fenetre = 20
        for i in range(len(df_dash) - fenetre):
            window = df_dash['count'].iloc[i:i+fenetre]
            if (window.mean() > seuil_congestion) and (window.std() < 2):
                congestion_frames += 1
        if congestion_frames > 0:
            st.error("⚠️ Embouteillage/congestion détecté sur plusieurs séquences de la vidéo.")
            st.markdown("""
            **Conseils d'amélioration du trafic :**
            - Adapter les horaires de circulation pour éviter les pics.
            - Mettre en place des feux intelligents ou une signalisation dynamique.
            - Encourager le covoiturage ou les transports en commun.
            - Optimiser la gestion des carrefours et des accès.
            """)
        else:
            st.success("Trafic fluide : pas de congestion détectée sur la période analysée.")
            st.markdown("""
            **Conseils :**
            - Maintenir les conditions actuelles.
            - Continuer la surveillance pour anticiper d'éventuels problèmes.
            """)
    st.info("Le tableau de bord s'actualise automatiquement après chaque analyse de vidéo.")
st.header('1️⃣ Téléversez une vidéo ou une image')
uploaded_file = st.file_uploader('Charger une vidéo (mp4) ou une image (jpg, png)', type=['mp4', 'jpg', 'png'])

if uploaded_file:
    if uploaded_file.type == 'video/mp4':
        st.video(uploaded_file)
    else:
        image = Image.open(uploaded_file)
        st.image(image, caption="Aperçu de l'image", use_column_width=True)
    st.info("Cliquez sur 'Analyser' pour lancer la détection de véhicules.")
    if st.button('Analyser', use_container_width=True):
        with st.spinner('Analyse en cours, veuillez patienter...'):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    files={"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Analyse terminée. Nombre total de véhicules détectés : {data['total_vehicles']}")
                    # Attendre que le CSV soit bien écrit sur le disque avant de recharger
                    import time
                    csv_path = 'resultats_api.csv'
                    max_wait = 5
                    waited = 0
                    while not os.path.exists(csv_path) and waited < max_wait:
                        time.sleep(0.5)
                        waited += 0.5
                    # Affichage de la vidéo annotée si disponible
                    if 'annotated_video' in data:
                        import tempfile
                        video_bytes = bytes.fromhex(data['annotated_video'])
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_vid:
                            tmp_vid.write(video_bytes)
                            tmp_vid_path = tmp_vid.name
                        st.video(tmp_vid_path)
                        with open(tmp_vid_path, 'rb') as f:
                            st.download_button(
                                label="📥 Télécharger la vidéo annotée",
                                data=f,
                                file_name='video_annotee.mp4',
                                mime='video/mp4',
                                use_container_width=True
                            )
                    # Forcer le rechargement du dashboard après analyse
                    st.experimental_rerun()
                else:
                    st.error(f"Erreur API : {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Erreur lors de l'appel à l'API : {e}")
else:
    st.warning("Veuillez téléverser une vidéo ou une image pour commencer l'analyse.")

# --- Footer ---
st.markdown('<div class="footer">Projet réalisé par <b>Mukalay Mufitwe Johnny</b> en collaboration avec <b>ISICOM TECH</b> | 2025</div>', unsafe_allow_html=True)
