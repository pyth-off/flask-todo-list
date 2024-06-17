import json
from itertools import count
from db import db
from sqlalchemy.sql import func
from sqlalchemy import asc
from list.model import List


class ListItem(db.Model):
    __tablename__ = 'list_item'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128), nullable=False)
    done = db.Column(db.Boolean(), default=False)
    prio = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey(List.id))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return json.dumps({k: str(v) for k, v in self.__dict__.items()})


def list_item_set_done(id):
    list_item = ListItem.query.filter_by(id=id).first()
    list_item.done = True
    db.session.add(list_item)
    db.session.commit()
    return id


def list_item_create(list_id, text, prio):
    list_item = ListItem()
    list_item.list_id = list_id
    list_item.text = text
    list_item.prio = prio
    db.session.add(list_item)
    db.session.commit()
    return list_item.id


def list_get_item_count(list_id):
    try:
        return len(list_item_find_by_list_id(list_id))
    except Exception as e:
        print(repr(e))


def list_item_find_by_list_id(list_id):
    try:
        return ListItem.query.filter_by(list_id=list_id, done=False).order_by(asc(ListItem.prio)).all()
    except Exception as e:
        print(repr(e))


def list_item_fix_priorities(list_id):
    new_prio = 0
    for item in list_item_find_by_list_id(list_id):
        item.prio = new_prio
        db.session.add(item)
        db.session.commit()
        new_prio = new_prio + 10
    return list_id
