
import librosa
import numpy as np
from transformers import pipeline

MODEL_NAME = "Hemgg/Deepfake-audio-detection"

# Load the AI model only once
audio_classifier = None


def get_model():
    global audio_classifier

    if audio_classifier is None:
        print("Loading AI deepfake detection model...")

        audio_classifier = pipeline(
            "audio-classification",
            model=MODEL_NAME
        )

        print("AI model loaded successfully!")

    return audio_classifier


def analyze_audio(file_path):
    try:
        # Load audio and convert to 16 kHz mono
        audio, sr = librosa.load(
            file_path,
            sr=16000,
            mono=True
        )

        if len(audio) < sr:
            return {
                "status": "error",
                "message": "Audio must be at least one second long."
            }

        duration = len(audio) / sr

        # Extract audio characteristics
        rms = float(
            np.mean(librosa.feature.rms(y=audio))
        )

        zero_crossing = float(
            np.mean(librosa.feature.zero_crossing_rate(audio))
        )

        spectral_centroid = float(
            np.mean(
                librosa.feature.spectral_centroid(
                    y=audio,
                    sr=sr
                )
            )
        )

        # Load pretrained AI model
        model = get_model()

        # Get model predictions
        predictions = model(
            {
                "raw": audio,
                "sampling_rate": sr
            },
            top_k=None
        )

        predictions = sorted(
            predictions,
            key=lambda item: item["score"],
            reverse=True
        )

        # Normalize labels for reliable matching
        def normalize_label(label):
            return (
                label.lower()
                .replace("_", "")
                .replace("-", "")
                .replace(" ", "")
            )

        fake_labels = {
            "aivoice",
            "fake",
            "synthetic",
            "spoof",
            "ai"
        }

        real_labels = {
            "humanvoice",
            "human",
            "real",
            "genuine",
            "bonafide"
        }

        fake_result = next(
            (
                item for item in predictions
                if normalize_label(item["label"]) in fake_labels
            ),
            None
        )

        real_result = next(
            (
                item for item in predictions
                if normalize_label(item["label"]) in real_labels
            ),
            None
        )

        if fake_result and real_result:

            fake_score = float(fake_result["score"])
            real_score = float(real_result["score"])

            prediction = (
                "POSSIBLY AI-GENERATED"
                if fake_score >= real_score
                else "LIKELY HUMAN SPEECH"
            )

            message = (
                "The model found a stronger AI-generated voice signal."
                if fake_score >= real_score
                else "The model found a stronger human voice signal."
            )

            model_status = "classified"

        else:
            prediction = "LABEL MAPPING NEEDS VERIFICATION"

            message = (
                "The model returned unexpected labels. "
                "The result cannot be safely classified."
            )

            fake_score = None
            real_score = None
            model_status = "unmapped"

        return {
            "status": "success",
            "model_status": model_status,
            "prediction": prediction,
            "message": message,
            "duration": round(duration, 2),
            "rms": round(rms, 4),
            "zero_crossing_rate": round(zero_crossing, 4),
            "spectral_centroid": round(
                spectral_centroid, 2
            ),
            "fake_score": (
                round(fake_score, 4)
                if fake_score is not None else None
            ),
            "real_score": (
                round(real_score, 4)
                if real_score is not None else None
            ),
            "raw_predictions": [
                {
                    "label": item["label"],
                    "score": round(float(item["score"]), 4)
                }
                for item in predictions
            ]
        }

    except Exception as error:
        return {
            "status": "error",
            "message": str(error)
        }
