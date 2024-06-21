import json

from db import db
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), default=None, nullable=True, onupdate=func.now())

    def __repr__(self):
        return json.dumps({k: str(v) for k, v in self.__dict__.items()})


def find_by_email(email):
    try:
        return User.query.filter_by(email=email, active=True).first()
    except Exception as e:
        print(repr(e))


def login(username, password):
    import hashlib
    user = User.query.filter_by(active=True, email=username, password=hashlib.sha3_512(password.encode('ascii')).hexdigest()).first()
    return False if user is None else True
