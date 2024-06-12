from index import db
from sqlalchemy.sql import func


class ListItem(db.Model):
    __tablename__ = 'list_item'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128), nullable=False)
    done = db.Column(db.Boolean(), default=True)
    prio = db.Column(db.Integer)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return 'Item Id:{} Text:{} List:{}'.format(self.id, self.text, self.list_id)
