from fastapi import FastAPI, File, UploadFile, HTTPException  # Import des modules FastAPI
import shutil  # Pour la gestion des fichiers temporaires
import os  # Pour la gestion des fichiers
import sys  # Pour modifier le chemin d'import Python
import cv2  # Pour la visualisation vidéo
import tempfile
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../model')))
from detection import VehicleDetector  # Importe la classe de détection

app = FastAPI()  # Création de l'application FastAPI

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    """
    Endpoint pour analyser une vidéo envoyée par l'utilisateur.
    Reçoit un fichier vidéo, effectue la détection, retourne le total de véhicules détectés, le chemin du CSV et une vidéo annotée.
    """
    temp_video_path = "temp_video.mp4"
    temp_annotated_path = "temp_annotated.mp4"
    try:
        # Sauvegarde temporaire de la vidéo reçue
        with open(temp_video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        # Création du détecteur et analyse de la vidéo avec sauvegarde vidéo annotée
        detector = VehicleDetector(model_path='yolov5s.pt', conf=0.3)
        # On force show=False pour éviter l'affichage serveur
        results = detector.detect_vehicles(temp_video_path, save_csv=True, output_csv='resultats_api.csv', show=False, save_video=True, output_video=temp_annotated_path)
        total_vehicles = sum([r['count'] for r in results])
        # Prépare la vidéo annotée à renvoyer
        with open(temp_annotated_path, "rb") as f:
            annotated_bytes = f.read()
        os.remove(temp_video_path)  # Nettoyage du fichier temporaire
        os.remove(temp_annotated_path)
        return {
            "message": "Vidéo reçue et analysée",
            "total_vehicles": total_vehicles,
            "csv_file": "resultats_api.csv",
            "annotated_video": annotated_bytes.hex()  # Encodage hexadécimal pour le transfert
        }
    except Exception as e:
        # Nettoyage en cas d'erreur
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        if os.path.exists(temp_annotated_path):
            os.remove(temp_annotated_path)
        raise HTTPException(status_code=500, detail=str(e))
