import sys
import os
from model.detection import VehicleDetector
import argparse
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description='Pipeline automatisé de détection de véhicules')
    parser.add_argument('--video', required=True, help='Chemin de la vidéo à analyser')
    parser.add_argument('--output', default='resultats_pipeline.csv', help='Fichier CSV de sortie')
    parser.add_argument('--model', default='yolov5s.pt', help='Modèle YOLO à utiliser')
    parser.add_argument('--conf', type=float, default=0.3, help='Seuil de confiance')
    args = parser.parse_args()

    detector = VehicleDetector(model_path=args.model, conf=args.conf)
    results = detector.detect_vehicles(args.video, save_csv=True, output_csv=args.output, show=False)
    print(f"Analyse terminée. Résultats sauvegardés dans {args.output}")
    df = pd.read_csv(args.output)
    print(f"Nombre total de frames : {len(df)}")
    print(f"Nombre total de véhicules détectés : {df['count'].sum()}")

if __name__ == '__main__':
    main()
