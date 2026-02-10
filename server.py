from flask import Flask, request, render_template
from emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/")
def render_index_page():
    return render_template('index.html')

# NOTE: to be honest, this API does not follow RESTful API best practieses.
# It would be better to accept only POST requests to /emotion-analysis
# with the text_to_analize parameter in the request body.
@app.get("/emotionDetector")
def detect_emotion():
    text_to_analyze = request.args.get("textToAnalyze", "").strip()
    predictions = emotion_detector(text_to_analyze)

    return (
        "For the given statement, the system response is "
        f"'anger': {predictions.anger}, 'disgust': {predictions.disgust},"
        f"'fear': {predictions.fear},'joy': {predictions.joy} and 'sadness': {predictions.sadness}. "
        f"The dominant emotion is {predictions.dominant_emotion}."
    )

if __name__ == "__main__":
    app.run(host="localhost", port=5000)