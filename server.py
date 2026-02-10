"""
This module provides Flask endpoints for an emotion detection service,
allowing clients to analyze text and retrieve predicted emotion scores
along with the dominant emotion.

Author: Mariia Khrustaleva
"""

from flask import Flask, render_template, request

from emotion_detection import emotion_detector

app = Flask(__name__)


@app.route("/")
def render_index_page():
    """
    Initiates the rendering of the main application
    page over the Flask channel
    """
    return render_template("index.html")


# NOTE-FOR-COURSE-TEAM: to be honest, this API does not follow RESTful API best practieses.
# It would be better to accept only POST requests to /emotion-analysis
# with the text_to_analize parameter in the request body.
@app.get("/emotionDetector")
def detect_emotion():
    """
    Handles GET requests to analyze the emotion of a text input.
    """
    text_to_analyze = request.args.get("textToAnalyze", "").strip()
    predictions = emotion_detector(text_to_analyze)
    if predictions.is_empty():
        # NOTE-FOR-COURSE-TEAM: To be honest, the server should not return a 200 status code here.
        # It should return a 400 status code, and the client code should be updated
        # to handle this case and display the corresponding error message.
        return "Invalid text! Please try again!"

    return (
        "For the given statement, the system response is "
        f"'anger': {predictions.anger}, 'disgust': {predictions.disgust},"
        f"'fear': {predictions.fear},'joy': {predictions.joy} and 'sadness': "
        f"{predictions.sadness}. The dominant emotion is {predictions.dominant_emotion}."
    )


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
