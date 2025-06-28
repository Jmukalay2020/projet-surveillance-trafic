import unittest  # Module de test unitaire Python
from model.detection import VehicleDetector  # Importe la classe à tester
import os  # Pour vérifier l'existence des fichiers
import tempfile
import shutil

# Classe de test unitaire pour le détecteur de véhicules
class TestVehicleDetector(unittest.TestCase):
    def setUp(self):
        # Initialise le détecteur avec un modèle et un seuil de confiance
        self.detector = VehicleDetector(model_path='yolov5s.pt', conf=0.3)
        self.test_video = '../test_video.mp4'  # Chemin vers une vidéo de test

    def test_detect_vehicles_output(self):
        # Vérifie que la vidéo de test existe
        if not os.path.exists(self.test_video):
            self.skipTest('Vidéo de test non trouvée')
        # Appelle la méthode de détection
        results = self.detector.detect_vehicles(self.test_video, save_csv=False, show=False)
        # Vérifie que le résultat est une liste
        self.assertIsInstance(results, list)
        # Vérifie que chaque élément contient les clés 'frame' et 'count'
        self.assertTrue(all('frame' in r and 'count' in r for r in results))

    def test_detect_vehicles_invalid_path(self):
        # Teste le comportement avec un chemin de vidéo invalide
        with self.assertRaises(Exception):
            self.detector.detect_vehicles('invalid_path.mp4', save_csv=False, show=False)

    def test_detect_vehicles_save_csv(self):
        # Vérifie la création d'un fichier CSV
        if not os.path.exists(self.test_video):
            self.skipTest('Vidéo de test non trouvée')
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, 'test_results.csv')
            results = self.detector.detect_vehicles(self.test_video, save_csv=True, output_csv=csv_path, show=False)
            self.assertTrue(os.path.exists(csv_path))
            self.assertGreater(len(results), 0)

if __name__ == '__main__':
    # Lance les tests unitaires
    unittest.main()
