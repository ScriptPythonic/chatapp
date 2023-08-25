from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(150))
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    phone = db.Column(db.String(11), nullable=True)
    profile_picture = db.Column(db.String(255))
    about = db.Column(db.String(255))


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='messages', foreign_keys=[user_id])
