import os
import requests
import operator
import re
import nltk
import json
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

def addTask(boardID, body, cardID, taskOrder):
    task  = tasks(boardID, body, cardID, taskOrder)
    db.session.add(task)
    db.session.commit()
    card  = cards.query.filter_by(id = cardID).first()
    card.numTasks=card.numTasks+1
    db.session.commit()

def populate():
    db.create_all()
    newBoard = boards()
    db.session.add(newBoard)
    db.session.commit()
    cardtest = cards(1, 1, 'card 1')
    db.session.add(cardtest)
    db.session.commit()
    cardtest = cards(1, 2, 'card 2')
    db.session.add(cardtest)
    db.session.commit()
    cardtest = cards(1, 3, 'card 3')
    db.session.add(cardtest)
    db.session.commit()
    cardtest = cards(1, 4, 'card 4')
    db.session.add(cardtest)
    db.session.commit()
    cardtest = cards(1, 5, 'card 5')
    db.session.add(cardtest)
    db.session.commit()
    addtasks(1,"task 1", 1, 1)
    addtasks(1,"task 1", 1, 2)
    addtasks(1,"task 1", 1, 3)
    addtasks(1,"task 1", 2, 1)
    addtasks(1,"task 1", 2, 2)
    addtasks(1,"task 1", 3, 1)

populate()
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
# cd=cards.query.all()
# td=tasks.query.all()
# print(cd)
# print(td)

@app.route("/", methods=["GET", "POST"])
def index():
    return ("hello world")

@app.route("/boardData", methods=["GET", "POST"])
def bd():
    b=boards.query.first()
    boardID = 1
    board={}
    board['cards']=[]
    board['id']=boardID
    thisBoard=boards.query.filter_by(id = board['id']).first()
    board['numCards']=thisBoard.numCards
    x=cards.query.filter_by(boardID = board['id']).all()
    for c in x:
        tempCard = {"id":c.id, 'title':c.title, 'numTasks':c.numTasks, 'created': c.created, 'cardOrder': c.cardOrder, 'boardID': c.boardID}
        tempTasks = []
        y=tasks.query.filter_by(cardID = c.id).all()
        for t in y:
            tempTask={'id': t.id, 'cardID': t.cardID, 'body': t.body, 'created': t.created, 'taskOrder':t.taskOrder, 'boardID':t.boardID}
            tempTasks.append(tempTask.copy())
        tempCard['tasks']=tempTasks
        board['cards'].append(tempCard.copy())
    board['cards'] = (sorted(board['cards'], key = lambda i: i['cardOrder']))
    return(jsonify(board))

@app.route("/updateCard", methods=["GET","POST"])
def updateCardTitle():
    title = request.form['title']
    cardID = request.form['id']
    card  = cards.query.filter_by(id = cardID).first()
    card.title=title
    db.session.commit()
    if request.method == 'POST':
        return('CARD EDIT RECIEVED')

@app.route("/updateTask", methods=["GET","POST"])
def updateTaskBody():
    body = request.form['body']
    taskID = request.form['id']
    task  = tasks.query.filter_by(id = taskID).first()
    task.body=body
    db.session.commit()
    if request.method == 'POST':
        return('TASK EDIT RECIEVED')

@app.route("/addCard", methods=["GET","POST"])
def addCard():
    boardID = request.form['boardID']
    cardOrder = request.form['cardOrder']
    title = request.form['title']
    card  = cards(boardID, cardOrder, title)
    db.session.add(card)
    db.session.commit()
    board  = boards.query.filter_by(id = boardID).first()
    board.numCards = board.numCards + 1
    if request.method == 'POST':
        return('CARD ADDITION RECIEVED')

@app.route("/addTask", methods=["GET","POST"])
def addTask():
    boardID = request.form['boardID']
    body = request.form['body']
    cardID = request.form['cid']
    taskOrder = request.form['torder']
    addTask(boardID, body, cardID, taskOrder)
    if request.method == 'POST':
        return('TASK ADDITION RECIEVED')


if __name__ == '__main__':
    app.run()