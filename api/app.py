from fastapi import FastAPI, File, UploadFile, HTTPException
import shutil
import os
import sys
sys.path.append('../model')
from detection import VehicleDetector

app = FastAPI()

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    temp_video_path = "temp_video.mp4"
    try:
        with open(temp_video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        detector = VehicleDetector(model_path='yolov5s.pt', conf=0.3)
        results = detector.detect_vehicles(temp_video_path, save_csv=True, output_csv='resultats_api.csv', show=False)
        total_vehicles = sum([r['count'] for r in results])
        os.remove(temp_video_path)
        return {
            "message": "Vidéo reçue et analysée",
            "total_vehicles": total_vehicles,
            "csv_file": "resultats_api.csv"
        }
    except Exception as e:
        if os.path.exists(temp_video_path):
            os.remove(temp_video_path)
        raise HTTPException(status_code=500, detail=str(e))
