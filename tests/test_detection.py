import unittest
from src.utils.eye_utils import eye_aspect_ratio

class TestDrowsinessDetection(unittest.TestCase):
    def test_eye_aspect_ratio(self):
        # Test case for eye aspect ratio calculation
        eye = [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
        ear = eye_aspect_ratio(eye)
        self.assertAlmostEqual(ear, 1.0)

if _name_ == "_main_":
    unittest.main()