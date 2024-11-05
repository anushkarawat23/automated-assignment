from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=True)
    assignment_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    deadline_date = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="Pending")

    def __repr__(self):
        return f'<Assignment {self.assignment_name}, {self.status}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Student {self.email}>'

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Admin {self.email}>'
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_topic = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    submission_date = db.Column(db.Date, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    file_path = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Question {self.assignment_topic}>'