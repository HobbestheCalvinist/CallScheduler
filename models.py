# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    contacts = db.relationship('Contact', backref='group', lazy=True)
    calls = db.relationship('Call', backref='group', lazy=True)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    calls_made = db.relationship('Call', foreign_keys='Call.caller_id', backref='caller', lazy=True)
    calls_received = db.relationship('Call', foreign_keys='Call.receiver_id', backref='receiver', lazy=True)

class Call(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.String(50), nullable=False)
    caller_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
