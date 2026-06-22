# ml_engine.py – Garud AI ML-Powered Spam Detection
# Loads the pre-trained Naive Bayes model + TF-IDF vectorizer
# and provides spam probability predictions.
#
# NOTE: This uses classical Machine Learning (Naive Bayes), NOT deep learning.
# Model must be trained first by running: python train_model.py

import pickle
import os

MODEL_PATH = "model.pkl"
VECTORIZER_PATH = "vectorizer.pkl"

_model = None
_vectorizer = None
_load_error = None


def _load_model():
    """Lazy-load the model and vectorizer (only once)."""
    global _model, _vectorizer, _load_error
    if _model is not None or _load_error is not None:
        return

    if not (os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)):
        _load_error = "Model files not found. Run 'python train_model.py' first."
        return

    try:
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)
        with open(VECTORIZER_PATH, "rb") as f:
            _vectorizer = pickle.load(f)
    except Exception as e:
        _load_error = f"Failed to load model: {e}"


def is_model_ready() -> bool:
    """Check whether the ML model is trained and loadable."""
    _load_model()
    return _model is not None and _vectorizer is not None


def get_load_error() -> str:
    """Return the reason the model isn't ready, if any."""
    return _load_error or ""


def predict_spam(text: str) -> dict:
    """
    Predict spam probability for a given text using the trained ML model.
    Returns a dict with score (0-100), level, and label (spam/ham).
    """
    _load_model()

    if not is_model_ready():
        return {
            "available": False,
            "score": 0,
            "level": "Unknown",
            "color": "#52525b",
            "label": "N/A",
            "error": _load_error,
        }

    # Transform input text using the same vectorizer used in training
    vec = _vectorizer.transform([text])

    # predict_proba returns [P(ham), P(spam)]
    proba = _model.predict_proba(vec)[0]
    spam_prob = proba[1]  # probability of being spam

    score = int(round(spam_prob * 100))

    if score >= 70:
        level, color = "High", "#ff4b4b"
    elif score >= 35:
        level, color = "Medium", "#ffb84b"
    else:
        level, color = "Low", "#00ffb4"

    return {
        "available": True,
        "score": score,
        "level": level,
        "color": color,
        "label": "Spam" if spam_prob >= 0.5 else "Ham (Safe)",
        "error": None,
    }
