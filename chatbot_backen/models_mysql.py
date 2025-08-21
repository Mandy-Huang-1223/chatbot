# models_mysql.py - MySQL version for PythonAnywhere
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class ChatRoom(db.Model):
    __tablename__ = 'chatrooms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    message_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to messages
    messages = db.relationship('Message', backref='chatroom_ref', lazy=True, cascade='all, delete-orphan')
    
    def to_json(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'message_count': self.message_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True)
    sender = db.Column(db.String(50), nullable=False)  # 'user' or 'ai'
    image = db.Column(db.String(255), nullable=True)  # filename for uploaded images
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key to chatroom
    chatRoom_id = db.Column(db.Integer, db.ForeignKey('chatrooms.id'), nullable=False)
    
    def to_json(self):
        return {
            'id': str(self.id),
            'text': self.text,
            'sender': self.sender,
            'image': self.image,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'chatRoom': str(self.chatRoom_id)
        }
