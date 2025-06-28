import cv2
from anonymisation import anonymize_faces_plates

input_video = '../data/traffic.mp4'
output_video = '../data/traffic_anonymized.mp4'

cap = cv2.VideoCapture(input_video)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = anonymize_faces_plates(frame)
    out.write(frame)

cap.release()
out.release()
print('Vidéo anonymisée enregistrée dans', output_video)
