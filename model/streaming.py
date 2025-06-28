import cv2  # Bibliothèque pour le traitement d'images et de vidéos

# Fonction pour streamer la vidéo depuis une source (webcam ou caméra IP)
def stream_video(source=0):
    cap = cv2.VideoCapture(source)  # Ouvre la source vidéo
    while cap.isOpened():
        ret, frame = cap.read()  # Lit une frame
        if not ret:
            break  # Fin du flux vidéo
        # Affiche chaque frame dans une fenêtre (ajouter la détection ici si besoin)
        cv2.imshow('Stream Trafic', frame)
        # Quitter la boucle si la touche 'q' est pressée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()  # Libère la ressource vidéo
    cv2.destroyAllWindows()  # Ferme toutes les fenêtres d'affichage

if __name__ == '__main__':
    # Lance le streaming depuis la webcam locale (0) ou une URL de caméra IP
    stream_video(0)
