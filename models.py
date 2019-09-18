from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class cards(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    # bid = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(), nullable=False)
    num_tasks = db.Column(db.Integer)
    corder=db.Column(db.Integer, nullable=True)


    def __init__(self, title, corder):
        self.title = title
        # self.bid = bid
        self.num_tasks=0
        self.corder=corder

    def __repr__(self):
        return '<id {}>'.format(self.id)

class tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body= db.Column(db.String(), nullable=False)
    torder=db.Column(db.Integer, nullable=False)

    def __init__(self, cid, body, torder):
        self.cid = cid
        self.body = body
        self.torder = torder

    def __repr__(self):
        return '<id {}>'.format(self.id)

class boards(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    num_cards = db.Column(db.Integer)