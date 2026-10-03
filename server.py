"""
server.py

Flask web application that exposes the emotion detector over HTTP.

Covers:
    Task 6 - Web deployment of the application using Flask
    Task 3 - Format the output of the application
    Task 7 - Incorporate error handling
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector")
def emo_detector():
    """
    GET /emotionDetector?textToAnalyze=<text>

    Runs the emotion detector on the given text and returns a
    human-readable, formatted string describing the scores and the
    dominant emotion.
    """
    text_to_analyze = request.args.get("textToAnalyze", "")

    result = emotion_detector(text_to_analyze)

    # ---- Task 7: if the analysis failed (blank/invalid input), say so ----
    if result["dominant_emotion"] is None:
        return "Invalid text! Please try again."

    # ---- Task 3: format the output for the end user ----
    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return response_text


@app.route("/")
def render_index_page():
    """Serve the front-end page for the application."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
