from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='Incomplete')
