from __future__ import annotations

import json
from decimal import Decimal
from typing import Literal, overload

import requests
from attrs import define, field
from attrs.setters import frozen


def to_decimal_or_none(value: float | None) -> Decimal | None:
    if value is None:
        return None

    return Decimal(str(value)).quantize(Decimal("0.00001"))


@define(kw_only=True)
class EmotionPredict:
    anger: Decimal | None = field(
        default=None, converter=to_decimal_or_none, on_setattr=frozen
    )
    disgust: Decimal | None = field(
        default=None, converter=to_decimal_or_none, on_setattr=frozen
    )
    fear: Decimal | None = field(
        default=None, converter=to_decimal_or_none, on_setattr=frozen
    )
    joy: Decimal | None = field(
        default=None, converter=to_decimal_or_none, on_setattr=frozen
    )
    sadness: Decimal | None = field(
        default=None, converter=to_decimal_or_none, on_setattr=frozen
    )

    dominant_emotion: str | None = field(default=None, init=False)

    def __attrs_post_init__(self):
        emotion_scores = self.scores
        if all(value is not None for value in emotion_scores.values()):
            self.dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        elif not all(value is None for value in emotion_scores.values()):
            raise ValueError(
                "Invalid initialization: either all emotion scores must be provided or none"
            )

    @property
    def scores(self) -> dict[str, Decimal | None]:
        return {
            "anger": self.anger,
            "disgust": self.disgust,
            "fear": self.fear,
            "joy": self.joy,
            "sadness": self.sadness,
        }

    def to_dict(self, *, only_scores: bool = False) -> dict[str, Decimal | str | None]:
        data = self.scores.copy()
        if not only_scores:
            data["dominant_emotion"] = self.dominant_emotion

        return data

    @classmethod
    def from_func_response(cls, data: str, /) -> EmotionPredict:
        try:
            parsed_data = json.loads(data)
            emotion_scores = parsed_data["emotionPredictions"][0]["emotion"]
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(
                "Invalid response received from the Emotion Predict function"
            ) from exc

        return cls(**emotion_scores)

    @classmethod
    def empty(cls) -> EmotionPredict:
        return cls()

    def is_empty(self) -> bool:
        return all(value is None for value in self.to_dict().values())


@overload
def emotion_detector(
    text_to_analyze: str,
    *,
    convert_to_dict: Literal[False] = False,
) -> EmotionPredict: ...


@overload
def emotion_detector(
    text_to_analyze: str,
    *,
    convert_to_dict: Literal[True],
) -> dict[str, Decimal | str | None]: ...


def emotion_detector(
    text_to_analyze: str,
    *,
    convert_to_dict: bool = False,
) -> EmotionPredict | dict[str, Decimal | str | None]:
    function_url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    json_data = {
        "raw_document": {
            "text": text_to_analyze,
        },
    }
    response = requests.post(function_url, json=json_data, headers=headers)
    if 400 == response.status_code:
        emotion_predict = EmotionPredict.empty()
    else:
        response.raise_for_status()
        emotion_predict = EmotionPredict.from_func_response(response.text)

    if convert_to_dict:
        return emotion_predict.to_dict()

    return emotion_predict
