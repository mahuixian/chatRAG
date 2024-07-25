from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Upload(db.Model):
    __tablename__ = 'uploads'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    file_name = db.Column(db.String(255), nullable=False, unique=True)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'file_name': self.file_name,
            'status': self.status,
            'created_at': self.created_at
        }
        

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=True)
    reply = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'username': self.username,
            'message': self.message,
            'reply': self.reply,
            'created_at': self.created_at
        }