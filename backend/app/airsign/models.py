

from app.extinsions import db
from flask import current_app


from sqlalchemy.sql import func


class Airsign(db.Model):
    __tablename__ = 'airsign'
    id = db.Column(db.Integer, primary_key=True,)
    account_id = db.Column(db.Integer, nullable=False)
    hash_0 = db.Column(db.BigInteger, nullable=False)

    user_register_time = db.Column(
        db.DateTime, default=func.now(),  nullable=False)
