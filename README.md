# DeepfakeShield 🛡️
### AI-Powered Deepfake Audio Analysis and Video Processing Platform

## 📌 About the Project
DeepfakeShield is an AI-powered web application designed to analyse potentially AI-generated audio and process video files. It aims to promote digital media security by helping users examine suspicious media content through audio analysis reports and video frame extraction.

## 🎯 Key Features
- **AI-Based Audio Detection:** Analyses uploaded audio files to identify potentially AI-generated voices.
- **Audio Analysis Report:** Displays AI Synthetic Score, Human Speech Score, audio duration and spectral characteristics.
- **Video Frame Extraction:** Extracts frames from uploaded video files for further examination.
- **Media Upload and Validation:** Supports multiple audio and video formats with file validation.
- **Analysis History:** Stores previous analysis records, including filenames, media types, results and timestamps.
- **User-Friendly Dashboard:** Provides a simple interface to access the platform's features.

## 🛠️ Technologies Used
- **Programming Language:** Python
- **Backend:** Flask
- **Frontend:** HTML, CSS, JavaScript
- **Audio Processing:** Python audio-processing libraries
- **Video Processing:** OpenCV
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Development Environment:** Visual Studio Code

## 📂 Project Structure
```text
DeepfakeShield/
│
├── app.py
├── detector.py
├── video_detector.py
├── history.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
├── static/
│   ├── hero.png
│   ├── script.js
│   └── style.css
│
└── .gitignore
```

## ⚙️ Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/DayanaBlessyA/DeepfakeShield.git
```

### 2. Navigate to the Project Folder
```bash
cd DeepfakeShield
```

### 3. Create a Virtual Environment
```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

### 6. Run the Application
```bash
python app.py
```

### 7. Open in Browser
```text
http://127.0.0.1:5000
```

## 📊 Current Prototype Status
- Audio analysis and report generation: Implemented.
- Video frame extraction: Implemented.
- Analysis history: Implemented.
- Video deepfake classification: Planned for future enhancement.

## 🚀 Future Enhancements
- Advanced video deepfake detection.
- Improved AI detection accuracy.
- Real-time media analysis.
- Enhanced security and reporting features.

## 👩‍💻 Developer
**Dayana Blessy A**

## 📄 License
This project is developed as a prototype for educational and innovation purposes.
