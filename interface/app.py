import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os
import folium
from streamlit_folium import st_folium

# --- En-tête stylisé et animation ---
st.set_page_config(page_title="ISICOM TRAFFIC CONTROL", page_icon="🚦", layout="centered")
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .isicom-title {
        font-size: 2.8em;
        font-weight: bold;
        color: #800000;
        letter-spacing: 2px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 18px;
        margin-bottom: 0.2em;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% {text-shadow: 0 0 0 #800000;}
        50% {text-shadow: 0 0 20px #800000;}
        100% {text-shadow: 0 0 0 #800000;}
    }
    .isicom-tech-icons {
        font-size: 1.5em;
        margin-left: 10px;
        color: #0072C6;
    }
    .stButton>button {background-color: #0072C6; color: white; font-weight: bold;}
    .stDownloadButton>button {background-color: #00B050; color: white; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="isicom-title">ISICOM <span style="color:#800000;">TRAFFIC CONTROL</span>'
    ' <span class="isicom-tech-icons">💻 📡 🤖 🚦</span></div>',
    unsafe_allow_html=True
)

# --- Carte de Kolwezi ---
st.header("🗺️ Carte de Kolwezi")
kolwezi_coords = (-10.7167, 25.4724)
map_kolwezi = folium.Map(location=kolwezi_coords, zoom_start=13)
st_folium(map_kolwezi, width=700, height=350)

# --- Calcul de trajet simple ---
st.header("🚗 Calcul de trajet à Kolwezi")
colA, colB = st.columns(2)
with colA:
    latA = st.number_input("Latitude point A", value=kolwezi_coords[0], format="%.6f")
    lonA = st.number_input("Longitude point A", value=kolwezi_coords[1], format="%.6f")
with colB:
    latB = st.number_input("Latitude point B", value=kolwezi_coords[0]+0.01, format="%.6f")
    lonB = st.number_input("Longitude point B", value=kolwezi_coords[1]+0.01, format="%.6f")
if st.button("Calculer le trajet", use_container_width=True):
    from geopy.distance import geodesic
    pointA = (latA, lonA)
    pointB = (latB, lonB)
    distance = geodesic(pointA, pointB).km
    st.success(f"Distance estimée entre A et B : {distance:.2f} km")
    # Affichage du trajet sur la carte
    trajet_map = folium.Map(location=kolwezi_coords, zoom_start=13)
    folium.Marker(pointA, tooltip="Point A", icon=folium.Icon(color='green')).add_to(trajet_map)
    folium.Marker(pointB, tooltip="Point B", icon=folium.Icon(color='red')).add_to(trajet_map)
    folium.PolyLine([pointA, pointB], color="blue", weight=3).add_to(trajet_map)
    st_folium(trajet_map, width=700, height=350)

# --- Analyse vidéo ---
st.header("1️⃣ Téléversement de la vidéo")
uploaded_file = st.file_uploader("Sélectionnez une vidéo au format MP4", type=["mp4"])
if uploaded_file is not None:
    st.video(uploaded_file)
    st.info("Cliquez sur 'Analyser' pour lancer la détection de véhicules.")
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
                    if 'csv_file' in data and os.path.exists('resultats_api.csv'):
                        df = pd.read_csv('resultats_api.csv')
                        st.header("2️⃣ Résultats de l'analyse")
                        col1, col2 = st.columns(2)
                        col1.metric("Nombre de frames analysées", len(df))
                        col2.metric("Total véhicules détectés", int(df['count'].sum()))
                        st.subheader("Évolution du trafic (véhicules/frame)")
                        st.line_chart(df['count'], use_container_width=True)
                        st.download_button(
                            label="📥 Télécharger les résultats (CSV)",
                            data=open('resultats_api.csv', 'rb'),
                            file_name='resultats_api.csv',
                            mime='text/csv',
                            use_container_width=True
                        )
                else:
                    st.error(f"Erreur API : {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Erreur lors de l'appel à l'API : {e}")
else:
    st.warning("Veuillez téléverser une vidéo pour commencer l'analyse.")

st.markdown("""
---
*Projet réalisé par **Mukalay Mufitwe Johnny** en collaboration avec **ISICOM TECH**.*
""")
