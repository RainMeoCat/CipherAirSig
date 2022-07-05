import uuid

from app.extinsions import db
from flask import current_app


from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,)
    user_nickname = db.Column(db.String(50),  nullable=False)
    user_password = db.Column(db.String(75), nullable=False)
    user_register_time = db.Column(
        db.DateTime, default=func.now(),  nullable=False)
