import unittest
from emotion_detection import emotion_detector

class TestEmotionDetection(unittest.TestCase):
    def test_joy_dominant_emotion(self):
        prediction = emotion_detector("I am glad this happened", convert_to_dict=False)
        self.assertEqual(prediction.dominant_emotion.lower(), "joy")
    
    def test_anger_dominant_emotion(self):
        prediction = emotion_detector("I am really mad about this", convert_to_dict=False)
        self.assertEqual(prediction.dominant_emotion.lower(), "anger")
    
    def test_disgust_dominant_emotion(self):
        prediction = emotion_detector("I feel disgusted just hearing about this", convert_to_dict=False)
        self.assertEqual(prediction.dominant_emotion.lower(), "disgust")
    
    def test_sadness_dominant_emotion(self):
        prediction = emotion_detector("I am so sad about this", convert_to_dict=False)
        self.assertEqual(prediction.dominant_emotion.lower(), "sadness")
    
    def test_fear_dominant_emotion(self):
        prediction = emotion_detector("I am really afraid that this will happen", convert_to_dict=False)
        self.assertEqual(prediction.dominant_emotion.lower(), "fear")


if __name__ == "__main__":
    unittest.main()