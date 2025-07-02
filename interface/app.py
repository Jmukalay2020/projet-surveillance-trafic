import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import folium
from streamlit_folium import st_folium
import pathlib

# --- En-tête stylisé et animation ---

st.set_page_config(page_title="ISICOM Traffic Control", page_icon="🚦", layout="wide")
st.markdown("""
    <style>
    body, .main {background: linear-gradient(120deg, #f5f7fa 0%, #e3e6ed 100%) !important;}
    .isicom-title {
        font-size: 2.5em;
        font-weight: 700;
        color: #0072C6;
        letter-spacing: 2px;
        text-align: center;
        margin-bottom: 0.2em;
        margin-top: 0.5em;
    }
    .isicom-sub {
        font-size: 1.1em;
        color: #444;
        text-align: center;
        margin-bottom: 1.5em;
    }
    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(90deg, #0072C6 0%, #00B050 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        font-size: 1.1em;
        margin-top: 0.5em;
    }
    .stSpinner > div > div {
        color: #0072C6 !important;
    }
    .result-block {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 12px #0072c61a;
        padding: 2em 2em 1em 2em;
        margin-top: 1.5em;
        margin-bottom: 2em;
    }
    .stMetric {
        background: #f5f7fa;
        border-radius: 8px;
        padding: 0.5em 0.5em;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="isicom-title">🚦 ISICOM TRAFFIC CONTROL</div>', unsafe_allow_html=True)
st.markdown('<div class="isicom-sub">Surveillance intelligente du trafic routier à Kolwezi</div>', unsafe_allow_html=True)


# --- Carte interactive et calcul de trajet ---
with st.expander("🗺️ Carte interactive de Kolwezi & Calcul de trajet", expanded=False):
    kolwezi_coords = (-10.7167, 25.4724)
    map_kolwezi = folium.Map(location=kolwezi_coords, zoom_start=13)
    st_folium(map_kolwezi, width=700, height=350)
    st.markdown("**Calculer la distance entre deux points :**")
    colA, colB = st.columns(2)
    with colA:
        latA = st.number_input("Latitude point A", value=kolwezi_coords[0], format="%.6f", key="latA")
        lonA = st.number_input("Longitude point A", value=kolwezi_coords[1], format="%.6f", key="lonA")
    with colB:
        latB = st.number_input("Latitude point B", value=kolwezi_coords[0]+0.01, format="%.6f", key="latB")
        lonB = st.number_input("Longitude point B", value=kolwezi_coords[1]+0.01, format="%.6f", key="lonB")
    if st.button("Calculer le trajet", key="trajet"):
        from geopy.distance import geodesic
        pointA = (latA, lonA)
        pointB = (latB, lonB)
        distance = geodesic(pointA, pointB).km
        st.success(f"Distance estimée entre A et B : {distance:.2f} km")
        trajet_map = folium.Map(location=kolwezi_coords, zoom_start=13)
        folium.Marker(pointA, tooltip="Point A", icon=folium.Icon(color='green')).add_to(trajet_map)
        folium.Marker(pointB, tooltip="Point B", icon=folium.Icon(color='red')).add_to(trajet_map)
        folium.PolyLine([pointA, pointB], color="blue", weight=3).add_to(trajet_map)
        st_folium(trajet_map, width=700, height=350)


# --- Analyse vidéo ---
st.markdown("""
<div style='background:#fff;border-radius:12px;padding:2em 2em 1em 2em;box-shadow:0 2px 12px #0072c61a;'>
<h3 style='color:#0072C6;margin-bottom:0.5em;'>1️⃣ Analyse de la circulation par vidéo</h3>
</div>
""", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Sélectionnez une vidéo au format MP4", type=["mp4"])
if uploaded_file is not None:
    st.video(uploaded_file, format="video/mp4", start_time=0)
    st.markdown("<style>video {max-width: 480px !important; height: auto !important; margin: 0 auto; display: block; border-radius: 10px; box-shadow: 0 2px 12px #0072c61a;}</style>", unsafe_allow_html=True)
    st.info("Appuyez sur 'Analyser' pour lancer la détection de véhicules sur la vidéo.")
    if st.button("Analyser", use_container_width=True):
        with st.spinner("Analyse en cours, veuillez patienter..."):
            try:
                response = requests.post(
                    "http://localhost:8000/analyze",
                    files={"file": (uploaded_file.name, uploaded_file, "video/mp4")}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ Analyse terminée. Nombre total de véhicules détectés : {data['total_vehicles']}")
                    racine = pathlib.Path(__file__).parent.parent.resolve()
                    csv_path = racine / 'resultats_api.csv'
                    if 'csv_file' in data and csv_path.exists():
                        df = pd.read_csv(csv_path)
                        if not df.empty:
                            st.markdown("""
                            <div class='result-block'>
                            <h4 style='color:#00B050;'>2️⃣ Tableau de bord du trafic</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            dash1, dash2, dash3, dash4 = st.columns(4)
                            dash1.metric("Frames analysées", len(df))
                            dash2.metric("Total véhicules", int(df['count'].sum()))
                            dash3.metric("Véhicules max/frame", int(df['count'].max()))
                            dash4.metric("Véhicules min/frame", int(df['count'].min()))
                            st.subheader("📊 Évolution du trafic (véhicules/frame)")
                            st.line_chart(df['count'], use_container_width=True)
                            st.subheader("📈 Histogramme du nombre de véhicules par frame")
                            st.bar_chart(df['count'].value_counts().sort_index(), use_container_width=True)
                            st.download_button(
                                label="📥 Télécharger les résultats (CSV)",
                                data=open(csv_path, 'rb'),
                                file_name='resultats_api.csv',
                                mime='text/csv',
                                use_container_width=True
                            )
                            # --- Analyse automatique de congestion/embouteillage ---
                            st.markdown("---")
                            st.header("🚦 Analyse de congestion et conseils")
                            congestion_frames = 0
                            seuil_congestion = df['count'].quantile(0.9)
                            fenetre = 20
                            for i in range(len(df) - fenetre):
                                window = df['count'].iloc[i:i+fenetre]
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
                            # --- Téléchargement vidéo annotée si disponible ---
                            if 'annotated_video' in data:
                                import tempfile, base64
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
                        else:
                            st.warning("Le fichier CSV généré est vide. Veuillez vérifier la vidéo ou réessayer.")
                    else:
                        st.warning("Aucun résultat trouvé. Le fichier CSV n'a pas été généré.")
                else:
                    st.error(f"Erreur API : {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Erreur lors de l'appel à l'API : {e}")
else:
    st.info("Veuillez téléverser une vidéo pour commencer l'analyse.")


st.markdown("""
---
<div style='text-align:center;font-size:1.1em;color:#888;'>
Projet réalisé par <b>Mukalay Mufitwe Johnny</b> avec <b>ISICOM TECH</b>.<br>
<span style='font-size:1.5em;'>🚦</span>
</div>
""", unsafe_allow_html=True)
