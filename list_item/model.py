import json
from itertools import count

from index import db
from sqlalchemy.sql import func

from list.model import List


class ListItem(db.Model):
    __tablename__ = 'list_item'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128), nullable=False)
    done = db.Column(db.Boolean(), default=True)
    prio = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey(List.id))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return json.dumps(self.__dict__)


def get_item_count(list_id):
    try:
        return count(ListItem.query.filter_by(list_id=list_id, active=False).all())
    except Exception as e:
        print(repr(e))


def find_by_list_id(list_id):
    try:
        return ListItem.query.filter_by(list_id=list_id, done=False).all()
    except Exception as e:
        print(repr(e))
