"""
emotion_detection.py

Emotion detection. Tries the Watson NLP Emotion Predict service first;
if it cannot be reached (for example outside the IBM lab), it falls back
to a simple local keyword-based detector so the app still works offline.
"""

import re

import requests

EMOTION_URL = (
    "https://sn-watson-emotion.labs.skills.network/v1/"
    "watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")

# Local fallback: words that signal each emotion. Words of 5+ letters also
# match their endings (e.g. "disgust" matches "disgusted").
LEXICON = {
    "anger": (
        "angry", "anger", "mad", "furious", "rage", "annoyed", "annoying",
        "irritated", "hate", "hated", "hates", "outraged", "livid",
        "resent", "fuming", "pissed", "infuriating",
    ),
    "disgust": (
        "disgust", "disgusting", "gross", "nasty", "revolting", "repulsive",
        "sickening", "vile", "yuck", "nauseating", "filthy", "appalling",
    ),
    "fear": (
        "afraid", "fear", "fearful", "scared", "scary", "terrified",
        "frightened", "anxious", "worried", "worry", "panic", "dread",
        "nervous", "horrified", "terrifying",
    ),
    "joy": (
        "happy", "glad", "joy", "joyful", "thrilled", "delighted",
        "excited", "love", "loved", "wonderful", "great", "cheerful",
        "pleased", "amazing", "awesome", "fantastic", "proud",
    ),
    "sadness": (
        "sad", "unhappy", "depressed", "cry", "crying", "miserable",
        "heartbroken", "grief", "lonely", "sorrow", "upset", "hopeless",
        "gloomy", "devastated",
    ),
}


def _empty_result():
    """Result returned for blank input or a failed request."""
    result = {emotion: None for emotion in EMOTIONS}
    result["dominant_emotion"] = None
    return result


def _local_detector(text):
    """Very simple offline detector: counts emotion words in the text."""
    words = re.findall(r"[a-z']+", text.lower())
    counts = {}
    for emotion in EMOTIONS:
        keywords = LEXICON[emotion]
        counts[emotion] = sum(
            1
            for word in words
            if any(
                word == key or (len(key) >= 5 and word.startswith(key))
                for key in keywords
            )
        )

    total = sum(counts.values())
    result = {
        emotion: round((counts[emotion] + 0.01) / (total + 0.05), 4)
        for emotion in EMOTIONS
    }
    result["dominant_emotion"] = max(EMOTIONS, key=lambda e: result[e])
    return result


def emotion_detector(text_to_analyze):
    """
    Analyze text and return the score of each emotion plus the dominant one.

    Returns a dict with every value set to None if the text is blank
    or the service answers with a 400 error.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        return _empty_result()

    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            EMOTION_URL, json=payload, headers=HEADERS, timeout=3
        )
    except requests.exceptions.RequestException:
        return _local_detector(text_to_analyze)

    if response.status_code == 400:
        return _empty_result()
    if response.status_code != 200:
        return _local_detector(text_to_analyze)

    scores = response.json()["emotionPredictions"][0]["emotion"]
    result = {emotion: scores[emotion] for emotion in EMOTIONS}
    result["dominant_emotion"] = max(EMOTIONS, key=lambda e: result[e])
    return result