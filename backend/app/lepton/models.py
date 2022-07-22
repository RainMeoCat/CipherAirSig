

from app.extinsions import db
from flask import current_app


from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import LONGTEXT


class Lepton(db.Model):
    __tablename__ = 'lepton'
    id = db.Column(db.Integer, primary_key=True,)
    base64_temperature = db.Column(LONGTEXT, nullable=False)
    confidence = db.Column(db.Integer, nullable=False)
    create_time = db.Column(
        db.DateTime, default=func.now(),  nullable=False)
