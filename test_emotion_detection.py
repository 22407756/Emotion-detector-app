"""
test_emotion_detection.py

Unit tests for the emotion_detector function.

Covers:
    Task 5 - Run unit tests on your application
"""

import unittest
from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Test suite validating the dominant emotion for known inputs."""

    def test_joy(self):
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result["dominant_emotion"], "joy")

    def test_anger(self):
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result["dominant_emotion"], "anger")

    def test_disgust(self):
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_sadness(self):
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_fear(self):
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result["dominant_emotion"], "fear")

    def test_blank_input(self):
        """Task 7 - blank input should be handled gracefully."""
        result = emotion_detector("")
        self.assertIsNone(result["dominant_emotion"])


if __name__ == "__main__":
    unittest.main()
