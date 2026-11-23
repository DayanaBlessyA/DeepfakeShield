
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class AnalysisHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    media_type = db.Column(db.String(20), nullable=False)
    prediction = db.Column(db.String(100), nullable=False)
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )
