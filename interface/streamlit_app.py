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
                    # Affichage de la vidéo annotée si disponible
                    if 'annotated_video' in data:
                        import tempfile, base64
                        video_bytes = bytes.fromhex(data['annotated_video'])
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_vid:
                            tmp_vid.write(video_bytes)
                            tmp_vid_path = tmp_vid.name
                        st.video(tmp_vid_path)
                    if 'csv_file' in data and os.path.exists('resultats_api.csv'):
                        df = pd.read_csv('resultats_api.csv')
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        col1.metric("Nombre de frames analysées", len(df))
                        col2.metric("Total véhicules détectés", int(df['count'].sum()))
                        st.line_chart(df['count'], use_container_width=True)
                        st.download_button(
                            label="📥 Télécharger les résultats (CSV)",
                            data=open('resultats_api.csv', 'rb'),
                            file_name='resultats_api.csv',
                            mime='text/csv',
                            use_container_width=True
                        )
                        # --- Dashboard analytique ---
                        st.markdown('---')
                        st.header('📊 Dashboard analytique')
                        st.subheader('Distribution des véhicules détectés')
                        st.bar_chart(df['count'].value_counts().sort_index(), use_container_width=True)
                        st.subheader('Statistiques')
                        st.write(f"Moyenne véhicules/frame : {df['count'].mean():.2f}")
                        st.write(f"Maximum véhicules sur une frame : {df['count'].max()}")
                        st.write(f"Minimum véhicules sur une frame : {df['count'].min()}")
                        st.write(f"Nombre de frames sans véhicule : {(df['count']==0).sum()}")
                        st.subheader('Histogramme du trafic')
                        st.pyplot(df['count'].plot(kind='hist', bins=20, color='#0072C6', edgecolor='black', alpha=0.7, title='Histogramme du nombre de véhicules par frame').get_figure())
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error(f"Erreur API : {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Erreur lors de l'appel à l'API : {e}")
else:
    st.warning("Veuillez téléverser une vidéo ou une image pour commencer l'analyse.")

# --- Footer ---
st.markdown('<div class="footer">Projet réalisé par <b>Mukalay Mufitwe Johnny</b> en collaboration avec <b>ISICOM TECH</b> | 2025</div>', unsafe_allow_html=True)
