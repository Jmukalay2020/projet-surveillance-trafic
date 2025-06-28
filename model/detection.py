import cv2  # Bibliothèque pour le traitement d'images et de vidéos
from ultralytics import YOLO  # Import du modèle YOLO pour la détection d'objets
import csv  # Pour l'écriture des résultats dans un fichier CSV
import os  # Pour la gestion des fichiers
import logging  # Ajout du module de logging

# Configuration du logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Classe pour la détection de véhicules à partir d'une vidéo
class VehicleDetector:
    def __init__(self, model_path='yolov5s.pt', conf=0.25):
        """
        Initialise le détecteur de véhicules avec un modèle YOLO et un seuil de confiance.
        model_path : chemin du modèle YOLO à utiliser
        conf : seuil de confiance pour la détection
        """
        logging.info(f"Chargement du modèle YOLO depuis {model_path}")
        self.model = YOLO(model_path)  # Chargement du modèle YOLO
        self.conf = conf  # Seuil de confiance

    def detect_vehicles(self, video_path, save_csv=False, output_csv='results.csv', show=True, save_video=False, output_video='annotated_output.mp4'):
        """
        Détecte les véhicules dans une vidéo.
        video_path : chemin de la vidéo à analyser
        save_csv : booléen, sauvegarder les résultats dans un CSV
        output_csv : nom du fichier CSV de sortie
        show : booléen, afficher la vidéo annotée en temps réel
        save_video : booléen, sauvegarder la vidéo annotée
        output_video : nom du fichier vidéo annoté
        Retourne une liste de dictionnaires avec le nombre de véhicules par frame.
        """
        if not os.path.exists(video_path):
            logging.error(f"Fichier vidéo non trouvé : {video_path}")
            raise FileNotFoundError(f"Fichier vidéo non trouvé : {video_path}")
        cap = cv2.VideoCapture(video_path)  # Ouvre la vidéo
        vehicle_counts = []  # Liste pour stocker les résultats
        frame_id = 0  # Compteur de frames
        writer = None
        if save_video:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
        logging.info(f"Début de la détection sur {video_path}")
        while cap.isOpened():
            ret, frame = cap.read()  # Lit une frame
            if not ret:
                break  # Fin de la vidéo
            # Application du modèle YOLO sur la frame courante
            results = self.model(frame, conf=self.conf)
            boxes = results[0].boxes  # Récupère les boîtes englobantes détectées
            count = len(boxes)  # Compte le nombre de véhicules détectés
            vehicle_counts.append({'frame': frame_id, 'count': count})  # Ajoute le résultat
            logging.debug(f"Frame {frame_id} : {count} véhicules détectés")
            # Génère une image annotée avec les détections
            annotated_frame = results[0].plot()
            if save_video and writer is not None:
                writer.write(annotated_frame)
            if show:
                cv2.imshow('Détection véhicules', annotated_frame)  # Affiche la frame annotée
                # Quitte la boucle si la touche 'q' est pressée
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            frame_id += 1  # Passe à la frame suivante
        cap.release()  # Libère la vidéo
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()  # Ferme les fenêtres d'affichage
        # Sauvegarde les résultats dans un fichier CSV si demandé
        if save_csv:
            with open(output_csv, 'w', newline='') as csvfile:
                writer_csv = csv.DictWriter(csvfile, fieldnames=['frame', 'count'])
                writer_csv.writeheader()
                writer_csv.writerows(vehicle_counts)
            logging.info(f"Résultats sauvegardés dans {output_csv}")
        logging.info(f"Détection terminée. Nombre total de frames traitées : {frame_id}")
        return vehicle_counts  # Retourne la liste des comptages
