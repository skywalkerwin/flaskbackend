from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class boards(db.Model):
    __tablename__ = 'boards'

    id = db.Column(db.Integer, primary_key=True)
    numCards = db.Column(db.Integer)

    def __init__(self):
        self.numCards = 0

    def __repr__(self):
        return '<id {}>'.format(self.id)


class cards(db.Model):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    boardID = db.Column(db.Integer, nullable=False)
    cardOrder=db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(), nullable=False)
    numTasks = db.Column(db.Integer)

    def __init__(self, boardID, cardOrder, title):
        self.boardID = boardID
        self.cardOrder=cardOrder
        self.numTasks=0
        self.title = title

    def __repr__(self):
        return '<id {}>'.format(self.id)


class tasks(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    boardID = db.Column(db.Integer, nullable=False)
    cardID = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body= db.Column(db.String(), nullable=False)
    taskOrder=db.Column(db.Integer, nullable=False)

    def __init__(self, boardID, body, cardID, taskOrder):
        self.boardID = boardID
        self.body = body
        self.cardID = cardID
        self.taskOrder = taskOrder

    def __repr__(self):
        return '<id {}>'.format(self.id)

