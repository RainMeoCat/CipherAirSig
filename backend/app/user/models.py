from app.extinsions import db
from flask import current_app


from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50), unique=True)
    account = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_name = db.Column(db.String(50),  nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(75), nullable=False)
    last_login = db.Column(db.DateTime, default=func.now(),  nullable=False)
    avatar = db.Column(db.String(200), nullable=True)
    register_time = db.Column(
        db.DateTime, default=func.now(),  nullable=False)
