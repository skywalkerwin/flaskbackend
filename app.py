import os
import requests
import operator
import re
import nltk
import json
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job
#from worker import conn
import collections
#https://realpython.com/flask-by-example-part-1-project-setup/
app = Flask(__name__)
CORS(app)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


from models import *

def addCard(boardID,  cardOrder, title):
    card  = cards(boardID, cardOrder, title)
    db.session.add(card)
    db.session.commit()
    board  = boards.query.filter_by(boardID = boardID).first()
    board.numCards=board.numCards + 1
    board.nextCardID = board.nextCardID + 1
    db.session.commit()
    return card

def addTask(boardID, body, cardID, taskOrder):
    task  = tasks(boardID, body, cardID, taskOrder)
    db.session.add(task)
    db.session.commit()
    card  = cards.query.filter_by(cardID = cardID).first()
    card.numTasks=card.numTasks+1
    db.session.commit()
    board = boards.query.filter_by(boardID = boardID).first()
    board.nextTaskID=board.nextTaskID+1
    db.session.commit()
    return task

def populate():
    db.create_all()
    newBoard = boards()
    db.session.add(newBoard)
    db.session.commit()
    addCard(1, 1, 'card 1')
    addCard(1, 2, 'card 2')

    addTask(1,"task 1", 1, 1)
    addTask(1,"task 1", 2, 1)

# populate()
# time.sleep(5);

# cd=cards.query.all()
# td=tasks.query.all()
# for t in td:
#     print (t.body,t.id)
#     db.session.delete(t)
#     db.session.commit()
# for c in cd:
#     print (c.title,c.id)
#     db.session.delete(c)
#     db.session.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    return ("hello world")

@app.route("/boardData", methods=["GET", "POST"])
def bd():
    b=boards.query.first()
    boardID = 1
    board={}
    board['cards']=[]
    board['boardID']=boardID
    thisBoard=boards.query.filter_by(boardID = board['boardID']).first()
    board['nextCardID'] = thisBoard.nextCardID
    board['nextTaskID'] = thisBoard.nextTaskID
    board['numCards'] = thisBoard.numCards
    x=cards.query.filter_by(boardID = board['boardID']).all()
    for c in x:
        tempCard = {"cardID":c.cardID, 'title':c.title, 'numTasks':c.numTasks, 'created': c.created, 'cardOrder': c.cardOrder, 'boardID': c.boardID}
        tempTasks = []
        y=tasks.query.filter_by(cardID = c.cardID).all()
        for t in y:
            tempTask={'taskID': t.taskID, 'cardID': t.cardID, 'body': t.body, 'created': t.created, 'taskOrder':t.taskOrder, 'boardID':t.boardID}
            tempTasks.append(tempTask.copy())
        tempCard['tasks']=tempTasks
        board['cards'].append(tempCard.copy())
    board['cards'] = (sorted(board['cards'], key = lambda i: i['cardOrder']))
    return(jsonify(board))

@app.route("/updateCard", methods=["GET","POST"])
def updateCardTitle():
    title = request.form['title']
    cardID = request.form['cardID']
    card  = cards.query.filter_by(cardID = cardID).first()
    card.title=title
    db.session.commit()
    if request.method == 'POST':
        return('CARD EDIT RECIEVED')

@app.route("/updateTask", methods=["GET","POST"])
def updateTaskBody():
    body = request.form['body']
    taskID = request.form['taskID']
    task  = tasks.query.filter_by(taskID = taskID).first()
    task.body=body
    db.session.commit()
    if request.method == 'POST':
        return('TASK EDIT RECIEVED')

@app.route("/addCard", methods=["GET","POST"])
def addCardAPI():
    boardID = request.form['boardID']
    cardOrder = request.form['cardOrder']
    title = request.form['title']
    c=addCard(boardID, cardOrder, title)
    tempCard = {"cardID":c.cardID, 'title':c.title, 'numTasks':c.numTasks, 'created': c.created, 'cardOrder': c.cardOrder, 'boardID': c.boardID}
    if request.method == 'POST':
        return(jsonify(tempCard))

@app.route("/addTask", methods=["GET","POST"])
def addTaskAPI():
    boardID = request.form['boardID']
    body = request.form['body']
    cardID = request.form['cardID']
    taskOrder = request.form['taskOrder']
    t=addTask(boardID, body, cardID, taskOrder)
    tempTask={'taskID': t.taskID, 'cardID': t.cardID, 'body': t.body, 'created': t.created, 'taskOrder':t.taskOrder, 'boardID':t.boardID}
    if request.method == 'POST':
        return(jsonify(tempTask))


if __name__ == '__main__':
    app.run()