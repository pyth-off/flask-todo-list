import json

from db import db
from sqlalchemy.sql import func
from user.model import User


class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return json.dumps({k: str(v) for k, v in self.__dict__.items()})


def delete(id):
    db.session.delete(find_by_id(id))
    db.session.commit()
    return id


def create(name, user_id):
    list = List()
    list.name = name
    list.user_id = user_id
    db.session.add(list)
    db.session.commit()
    return list.id


def find_by_id(list_id):
    try:
        return List.query.filter_by(id=list_id, active=True).first()
    except Exception as e:
        print(repr(e))


def find_by_user_id(user_id):
    try:
        return List.query.filter_by(user_id=user_id).all()
    except Exception as e:
        print(repr(e))
