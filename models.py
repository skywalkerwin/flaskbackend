from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class boards(db.Model):
    __tablename__ = 'boards'

    boardID = db.Column(db.Integer, primary_key=True)
    nextCardID = db.Column(db.Integer)
    nextTaskID = db.Column(db.Integer)
    numCards = db.Column(db.Integer)

    def __init__(self):
        self.numCards = 0
        self.nextCardID = 1
        self.nextTaskID = 1


    def __repr__(self):
        return '<id {}>'.format(self.boardID)


class cards(db.Model):
    __tablename__ = 'cards'

    cardID = db.Column(db.Integer, primary_key=True)
    boardID = db.Column(db.Integer, nullable=False)
    cardOrder=db.Column(db.Integer, nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(), nullable=False)
    numTasks = db.Column(db.Integer)

    def __init__(self, boardID, cardOrder, title):
        self.boardID = boardID
        # self.cardID=cardID
        self.cardOrder=cardOrder
        # self.created = created
        self.numTasks=0
        self.title = title

    def __repr__(self):
        return '<id {}>'.format(self.cardID)


class tasks(db.Model):
    __tablename__ = 'tasks'

    taskID = db.Column(db.Integer, primary_key=True)
    boardID = db.Column(db.Integer, nullable=False)
    cardID = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    body= db.Column(db.String(), nullable=False)
    taskOrder=db.Column(db.Integer, nullable=False)

    def __init__(self, boardID, body, cardID, taskOrder):
        self.boardID = boardID
        self.body = body
        # self.created = created
        self.cardID = cardID
        # self.taskID = taskID
        self.taskOrder = taskOrder

    def __repr__(self):
        return '<id {}>'.format(self.taskID)

