

from app.extinsions import db
from flask import current_app


from sqlalchemy.sql import func


class CR(db.Model):
    __tablename__ = 'cr'
    id = db.Column(db.Integer, primary_key=True,)
    account_id = db.Column(db.Integer, nullable=False)
    cr_token = db.Column(db.String(75), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    symbol_code = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    create_time = db.Column(
        db.DateTime, default=func.now(),  nullable=False)
