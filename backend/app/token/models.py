from app.extinsions import db
from flask import current_app


from sqlalchemy.sql import func


class Token(db.Model):
    __tablename__ = 'token'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer,  db.ForeignKey('user.id'))
    phase = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(75), nullable=False)
    token_enabled = db.Column(db.Boolean, default=True)
    create_time = db.Column(db.DateTime, default=func.now(),  nullable=False)
