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
    board.numTasks=board.numTasks+1
    db.session.commit()
    return task

def populate():
    db.create_all()
    newBoard = boards()
    db.session.add(newBoard)
    db.session.commit()
    # addCard(1, 1, 'card 1')
    # addCard(1, 2, 'card 2')

    # addTask(1,"task 1", 1, 1)
    # addTask(1,"task 1", 2, 1)

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
    board['numCards'] = thisBoard.numCards
    board['numTasks'] = thisBoard.numTasks
    x=cards.query.filter_by(boardID = board['boardID']).all()
    for c in x:
        tempCard = {"cardID":c.cardID, 'title':c.title, 'numTasks':c.numTasks, 'created': c.created, 'cardOrder': c.cardOrder, 'boardID': c.boardID}
        tempTasks = []
        y=tasks.query.filter_by(cardID = c.cardID).all()
        for t in y:
            tempTask={'taskID': t.taskID, 'cardID': t.cardID, 'body': t.body, 'created': t.created, 'taskOrder':t.taskOrder, 'boardID':t.boardID}
            tempTasks.append(tempTask.copy())
        tempCard['tasks']=sorted(tempTasks, key = lambda i: i['taskOrder'])
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
    # cardOrder = request.form['cardOrder']
    title = request.form['title']
    board = boards.query.filter_by(boardID = boardID).first()
    board.numCards=board.numCards+1
    db.session.commit()
    cardOrder=board.numCards
    c=addCard(boardID, cardOrder, title)
    tempCard = {"cardID":c.cardID, 'title':c.title, 'numTasks':c.numTasks, 'created': c.created, 'cardOrder': c.cardOrder, 'boardID': c.boardID}
    if request.method == 'POST':
        return(jsonify(tempCard))

@app.route("/addTask", methods=["GET","POST"])
def addTaskAPI():
    boardID = int(request.form['boardID'])
    body = request.form['body']
    cardID = int(request.form['cardID'])
    card  = cards.query.filter_by(cardID = cardID).first()
    card.numCards=card.numTasks+1
    db.session.commit()
    taskOrder = card.numTasks+1
    print(taskOrder)
    t=addTask(boardID, body, cardID, taskOrder)
    tempTask={'taskID': t.taskID, 'cardID': t.cardID, 'body': t.body, 'created': t.created, 'taskOrder':t.taskOrder, 'boardID':t.boardID}
    if request.method == 'POST':
        return(jsonify(tempTask))

@app.route("/deleteCard", methods=["GET","POST"])
def deleteCardAPI():
    cardID = request.form['cardID']
    c = cards.query.filter_by(cardID = cardID).first()
    ctasks = tasks.query.filter_by(cardID = cardID).all()
    for t in ctasks:
        print(t, t.body, t.taskID, t.cardID)
        db.session.delete(t)
        db.session.commit()
        c.numTasks=c.numTasks-1
        db.session.commit()
    db.session.delete(c)
    db.session.commit()
    board = boards.query.filter_by(boardID = c.boardID).first()
    board.numCards=board.numCards-1
    db.session.commit()

    if request.method == 'POST':
        return({'msg': 'Card and its tasks deleted'})

@app.route("/deleteTask", methods=["GET","POST"])
def deleteTaskAPI():
    taskID = request.form['taskID']
    t = tasks.query.filter_by(taskID = taskID).first()
    board = boards.query.filter_by(boardID = t.boardID).first()
    cardID = t.cardID
    taskOrder = t.taskOrder
    db.session.delete(t)
    db.session.commit()
    board.numTasks=board.numTasks-1
    db.session.commit()
    c = cards.query.filter_by(cardID = cardID).first()
    ctasks = tasks.query.filter_by(cardID = cardID).all()
    for t in ctasks:
        if (t.taskOrder>taskOrder):
            t.taskOrder=t.taskOrder-1
            db.session.commit()        
    c.numTasks=c.numTasks-1
    db.session.commit()
    if request.method == 'POST':
        return({'msg': 'Task deleted'})

@app.route("/moveTask", methods=["GET","POST"])
def moveTaskAPI():
    taskID = int(request.form['taskID'])
    droppedID = int(request.form['droppedID'])
    newCardID = int(request.form['cardID'])
    task = tasks.query.filter_by(taskID = taskID).first()
    card = cards.query.filter_by(cardID = task.cardID).first()
    dropcase=droppedID
    if(droppedID == 0 or droppedID == -1):
        droppedID=taskID
    droppedTask = tasks.query.filter_by(taskID = droppedID).first()
    dragOrder=task.taskOrder
    dropOrder=droppedTask.taskOrder
    oldCardID = task.cardID
    if (newCardID == oldCardID):
        ctasks = tasks.query.filter_by(cardID = task.cardID).all()
        if(dropcase==-1):
            # lift t>drag , drag = card.numtasks
            for t in ctasks:
                if(t.taskOrder>task.taskOrder):
                    t.taskOrder=t.taskOrder-1
                    db.session.commit()
            task.taskOrder=card.numTasks
            db.session.commit()
        elif(dropcase==0):
            # lower t< drag, drag = 0
            for t in ctasks:
                if(t.taskOrder<task.taskOrder):
                    t.taskOrder=t.taskOrder+1
                    db.session.commit()
            task.taskOrder=1
            db.session.commit()
        elif(task.taskOrder < droppedTask.taskOrder):
            #lift t>drag & t<=drop up...drag == drop
            for t in ctasks:
                if (t.taskOrder > task.taskOrder and t.taskOrder <= droppedTask.taskOrder):
                    t.taskOrder=t.taskOrder-1
                    db.session.commit()
            task.taskOrder=dropOrder
            db.session.commit()
        elif(task.taskOrder > droppedTask.taskOrder):
            #lower t>drop & t< drag...drag = drop+1
            for t in ctasks:
                if (t.taskOrder < task.taskOrder and t.taskOrder > droppedTask.taskOrder):
                    t.taskOrder=t.taskOrder+1
                    db.session.commit()
            task.taskOrder=dropOrder+1
            db.session.commit()

    # db.session.delete(t)
    # db.session.commit()
    # c = cards.query.filter_by(cardID = cardID).first()
    # ctasks = tasks.query.filter_by(cardID = cardID).all()
    # for t in ctasks:
    #     if (t.taskOrder>taskOrder):
    #         t.taskOrder=t.taskOrder-1
    #         db.session.commit()        
    # c.numTasks=c.numTasks-1
    # db.session.commit()
    if request.method == 'POST':
        return({'msg': 'Task Moved'})


if __name__ == '__main__':
    app.run()