import cv2
from ultralytics import YOLO
import csv
import os

class VehicleDetector:
    def __init__(self, model_path='yolov5s.pt', conf=0.25):
        self.model = YOLO(model_path)
        self.conf = conf

    def detect_vehicles(self, video_path, save_csv=False, output_csv='results.csv', show=True):
        cap = cv2.VideoCapture(video_path)
        vehicle_counts = []
        frame_id = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            results = self.model(frame, conf=self.conf)
            boxes = results[0].boxes
            count = len(boxes)
            vehicle_counts.append({'frame': frame_id, 'count': count})
            annotated_frame = results[0].plot()
            if show:
                cv2.imshow('Détection véhicules', annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            frame_id += 1
        cap.release()
        cv2.destroyAllWindows()
        if save_csv:
            with open(output_csv, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=['frame', 'count'])
                writer.writeheader()
                writer.writerows(vehicle_counts)
        return vehicle_counts
