
import os

from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from detector import analyze_audio
from video_detector import extract_video_frames
from history import db, AnalysisHistory


app = Flask(__name__)

# DATABASE CONFIGURATION
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///deepfake_history.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# FILE CONFIGURATION
UPLOAD_FOLDER = "uploads"

AUDIO_EXTENSIONS = {"wav", "mp3", "ogg", "flac"}
VIDEO_EXTENSIONS = {"mp4", "avi", "mov", "mkv", "webm"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# FILE VALIDATION
def allowed_file(filename, extensions):
    return (
        "." in filename and
        filename.rsplit(".", 1)[1].lower() in extensions
    )


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# AUDIO ANALYSIS
@app.route("/analyze", methods=["POST"])
def analyze():

    if "audio" not in request.files:
        return jsonify({"error": "No audio file selected."}), 400

    file = request.files["audio"]

    if file.filename == "":
        return jsonify({"error": "Please select an audio file."}), 400

    if not allowed_file(file.filename, AUDIO_EXTENSIONS):
        return jsonify({"error": "Unsupported audio format."}), 400

    filename = secure_filename(file.filename)

    if not filename:
        return jsonify({"error": "Invalid filename."}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        file.save(file_path)

        result = analyze_audio(file_path)

        record = AnalysisHistory(
            filename=filename,
            media_type="Audio",
            prediction=result.get("prediction", "Unknown")
        )

        db.session.add(record)
        db.session.commit()

        return jsonify(result)

    except Exception as error:
        db.session.rollback()

        return jsonify({
            "error": str(error)
        }), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# VIDEO ANALYSIS
@app.route("/analyze-video", methods=["POST"])
def analyze_video():

    if "video" not in request.files:
        return jsonify({"error": "No video file selected."}), 400

    file = request.files["video"]

    if file.filename == "":
        return jsonify({"error": "Please select a video."}), 400

    if not allowed_file(file.filename, VIDEO_EXTENSIONS):
        return jsonify({"error": "Unsupported video format."}), 400

    filename = secure_filename(file.filename)

    if not filename:
        return jsonify({"error": "Invalid filename."}), 400

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        file.save(file_path)

        result = extract_video_frames(file_path)

        record = AnalysisHistory(
            filename=filename,
            media_type="Video",
            prediction="Frames Extracted - Detection Pending"
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Video frames extracted successfully!",
            "total_frames": result["total_frames"],
            "extracted_frames": result["extracted_frames"]
        })

    except Exception as error:
        db.session.rollback()

        return jsonify({
            "status": "error",
            "error": str(error)
        }), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


# ANALYSIS HISTORY
@app.route("/history-data")
def history_data():

    records = AnalysisHistory.query.order_by(
        AnalysisHistory.created_at.desc()
    ).all()

    history = []

    for record in records:
        history.append({
            "id": record.id,
            "filename": record.filename,
            "media_type": record.media_type,
            "prediction": record.prediction,
            "created_at": record.created_at.strftime(
                "%d-%m-%Y %H:%M"
            )
        })

    return jsonify(history)


# FILE SIZE ERROR
@app.errorhandler(413)
def file_too_large(error):

    return jsonify({
        "error": "File size must be below 100 MB."
    }), 413


# RUN APPLICATION
if __name__ == "__main__":
    app.run(debug=True)
