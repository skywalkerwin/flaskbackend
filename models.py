from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class cards(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=false, default=datetime.utcnow)
    title = db.Column(db.String(), nullable=false)
    num_tasks = db.Column(db.Integer)
    tasks=db.relationship('Tasks', backref='card', lazy=True)

    def __init__(self, title):
        self.title = title
        self.num_tasks=0

    def __repr__(self):
        return '<id {}>'.format(self.id)

class tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('card.id', nullable=false)
    created = db.Column(db.DateTime, nullable=false, default=datetime.utcnow)
    body= db.Column(db.string(), nullable=false)
    torder=db.Column(db.Integer, nullable=false)

    def __init__(self, pcard, body, torder):
        self.pcard = pcard
        self.body = body
        self.torder = torder

    def __repr__(self):
        return '<id {}>'.format(self.id)