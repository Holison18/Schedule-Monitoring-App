from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Pair(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pair_name = db.Column(db.String(100), unique=True, nullable=False)
    user1_email = db.Column(db.String(120), nullable=False)
    user2_email = db.Column(db.String(120))

    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    schools = db.relationship('School', backref='assigned_pair', lazy=True)
    schedules = db.relationship('Schedule', backref='pair', lazy=True)

class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(200), nullable=False)  
    region = db.Column(db.String(100))
    district = db.Column(db.String(100))
    location = db.Column(db.String(100))
    school_code = db.Column(db.String(50), unique=False, nullable=True) 
    head_teacher_name  = db.Column(db.String(100)) 
    head_teacher_contact  = db.Column(db.String(30))
    
    pair_id = db.Column(db.Integer, db.ForeignKey('pair.id'), nullable=False)
    schedule = db.relationship('Schedule', backref='school', uselist=False)


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    pair_id = db.Column(db.Integer, db.ForeignKey('pair.id'), nullable=False)
    contacted_school = db.Column(db.Boolean, default=False)
    reason_if_not_contacted = db.Column(db.Text)
    headmaster_name_on_schedule = db.Column(db.String(100))
    headmaster_contact_on_schedule = db.Column(db.String(20))
    scheduled_date = db.Column(db.Date)
    created_by = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)