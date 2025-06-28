import unittest  # Module de test unitaire Python
from detection import detect_vehicles  # Importe la fonction à tester

# Classe de test unitaire pour la fonction de détection de véhicules
class TestDetection(unittest.TestCase):
    def test_detect_vehicles_on_sample(self):
        # Chemin vers une vidéo de test (à adapter selon vos données)
        image_path = '../data/traffic.mp4'
        # Appel de la fonction de détection
        result = detect_vehicles(image_path)
        # Vérifie que le résultat est bien une liste
        self.assertIsInstance(result, list)
        # Ajouter d'autres assertions selon le format attendu

if __name__ == '__main__':
    # Lance les tests unitaires
    unittest.main()
