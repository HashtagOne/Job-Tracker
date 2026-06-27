from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    jobs = db.relationship("JobApplication", backref="owner", cascade="all, delete-orphan")

class JobApplication(db.Model):
    __tablename__="job_applications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Applied")
    date_applied = db.Column(db.Date, nullable=False)
    link = db.Column(db.String(300), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "role": self.role,
            "status": self.status,
            "date_applied": self.date_applied.isoformat(),
            "link": self.link,
            "notes": self.notes,
            "created_at": self.created_at.isoformat()
        }