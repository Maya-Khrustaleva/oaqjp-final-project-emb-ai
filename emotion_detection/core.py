import requests
import json
from attrs import define, field
from attrs.setters import frozen
from decimal import Decimal, getcontext

def to_decimal(value: float) -> Decimal:
    return Decimal(value).quantize(Decimal("0.00001"))

@define(kw_only=True)
class EmotionPredict:
    anger: Decimal = field(converter=to_decimal, on_setattr=frozen)
    disgust: Decimal = field(converter=to_decimal, on_setattr=frozen)
    fear: Decimal = field(converter=to_decimal, on_setattr=frozen)
    joy: Decimal = field(converter=to_decimal, on_setattr=frozen)
    sadness: Decimal = field(converter=to_decimal, on_setattr=frozen)

    dominant_emotion: str = field(init=False)

    def __attrs_post_init__(self):
        emotion_scores = self.scores
        self.dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    @property
    def scores(self) -> dict[str, Decimal]:
        return {
            "anger": self.anger,
            "disgust": self.disgust,
            "fear": self.fear,
            "joy": self.joy,
            "sadness": self.sadness,
        }

    def to_dict(self, *, only_scores: bool = False) -> dict[str, Decimal | str]:
        data = self.scores.copy()
        if not only_scores:
            data["dominant_emotion"] = self.dominant_emotion

        return data

    @classmethod
    def from_func_response(cls, data: str, /):
        parsed_data = json.loads(data)
        try:
            parsed_data = json.loads(data)
            emotion_scores = parsed_data["emotionPredictions"][0]["emotion"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError("Invalid response received from the Emotion Predict function") from exc

        return cls(**emotion_scores)

def emotion_detector(
    text_to_analyze: str,
    *,
    convert_to_dict: bool = True,
) -> dict[str, Decimal | str]:
    function_url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    json_data = {
        "raw_document": {
            "text": text_to_analyze,
        },
    }
    response = requests.post(function_url, json=json_data, headers=headers)
    emotion_predict = EmotionPredict.from_func_response(response.text)
    
    if convert_to_dict:
        return emotion_predict.to_dict()
    return emotion_predict