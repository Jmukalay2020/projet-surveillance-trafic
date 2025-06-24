import unittest
from model.detection import VehicleDetector
import os

class TestVehicleDetector(unittest.TestCase):
    def setUp(self):
        self.detector = VehicleDetector(model_path='yolov5s.pt', conf=0.3)
        self.test_video = '../test_video.mp4'  # Remplacez par un chemin de vidéo de test valide

    def test_detect_vehicles_output(self):
        if not os.path.exists(self.test_video):
            self.skipTest('Vidéo de test non trouvée')
        results = self.detector.detect_vehicles(self.test_video, save_csv=False, show=False)
        self.assertIsInstance(results, list)
        self.assertTrue(all('frame' in r and 'count' in r for r in results))

if __name__ == '__main__':
    unittest.main()
