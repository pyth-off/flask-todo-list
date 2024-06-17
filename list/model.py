from index import db
from sqlalchemy.sql import func
from user.model import User


class List(db.Model):
    __tablename__ = 'list'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    def __repr__(self):
        return 'List Id:{} Name:{} User:{}'.format(self.id, self.name, self.user_id)


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
