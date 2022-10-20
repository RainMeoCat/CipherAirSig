from app.extinsions import db
from flask import current_app


from sqlalchemy.sql import func


class Gsign(db.Model):
    __tablename__ = 'gsign'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer,  db.ForeignKey('user.id'))
