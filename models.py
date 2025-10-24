from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    complaints = db.relationship('Complaint', backref='user', lazy=True, foreign_keys='Complaint.user_id')
    assigned_complaints = db.relationship('Complaint', backref='contractor', lazy=True, foreign_keys='Complaint.contractor_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contractor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    district = db.Column(db.String(100), nullable=False)
    corporation_type = db.Column(db.String(50), nullable=False)
    road_name = db.Column(db.String(200), nullable=False)
    national_highway = db.Column(db.String(100))
    landmark = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.Text, nullable=False)
    
    status = db.Column(db.String(50), default='Submitted')
    admin_acknowledgement = db.Column(db.Text)
    contractor_acknowledgement = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    verified_at = db.Column(db.DateTime)
    assigned_at = db.Column(db.DateTime)
    resolved_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Complaint {self.id} - {self.status}>'
