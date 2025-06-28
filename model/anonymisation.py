import cv2  # Bibliothèque pour le traitement d'images

# Fonction pour anonymiser les visages et plaques sur une image
# (à compléter avec la détection automatique des régions à flouter)
def anonymize_faces_plates(image):
    # TODO: Détecter et flouter les visages et plaques
    # Exemple de floutage sur une région (x, y, w, h)
    # x, y, w, h = 100, 100, 50, 50
    # roi = image[y:y+h, x:x+w]
    # image[y:y+h, x:x+w] = cv2.GaussianBlur(roi, (51, 51), 0)
    return image  # Retourne l'image (modifiée ou non)
