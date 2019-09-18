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
# db.create_all()
# cardtest = cards('card 1',1)
# db.session.add(cardtest)
# db.session.commit()
# cardtest = cards('card 2',2)
# db.session.add(cardtest)
# db.session.commit()
# cardtest = cards('card 3',3)
# db.session.add(cardtest)
# db.session.commit()
# tasktest = tasks(34,"task 1", 1)
# db.session.add(tasktest)
# db.session.commit()
# tasktest = tasks(34,"task 2", 2)
# db.session.add(tasktest)
# db.session.commit()
# tasktest = tasks(34,"task 3", 3)
# db.session.add(tasktest)
# db.session.commit()
# tasktest = tasks(35,"task 1", 1)
# db.session.add(tasktest)
# db.session.commit()
# tasktest = tasks(35,"task 2", 2)
# db.session.add(tasktest)
# db.session.commit()
# tasktest = tasks(36,"task 1", 1)
# db.session.add(tasktest)
# db.session.commit()

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
    board={}
    board['cards']=[]
    # board['tasks']=[]
    x=cards.query.all()
    y=tasks.query.all()
    for c in x:
        # tempCard = [c.id, c.title, c.num_tasks, c.created]
        tempCard = {"id":c.id, 'title':c.title, 'num_tasks':c.num_tasks, 'created': c.created, 'corder': c.corder}
        tempTasks = []
        for t in y:
            if(t.cid==c.id):
                tempTask={'id': t.id, 'cid': t.cid, 'body': t.body, 'created': t.created, 'torder':t.torder}
                tempTasks.append(tempTask.copy())
        tempCard['tasks']=tempTasks
        board['cards'].append(tempCard.copy())
    board['cards'] = (sorted(board['cards'], key = lambda i: i['corder']))
    # for c in x:
    #     board['cards'].append([c.id, c.title, c.num_tasks, c.created])
    # for t in y:
    #     board['tasks'].append([t.id, t.cid, t.body, t.created, t.torder])
    return(jsonify(board))

@app.route("/updateCard", methods=["GET","POST"])
def updateCardTitle():
    title = request.form['title']
    cid = request.form['id']
    card  = cards.query.filter_by(id = cid).first()
    card.title=title
    db.session.commit()
    if request.method == 'POST':
        return('CARD EDIT RECIEVED')

@app.route("/updateTask", methods=["GET","POST"])
def updateTaskBody():
    body = request.form['body']
    tid = request.form['id']
    task  = tasks.query.filter_by(id = tid).first()
    task.body=body
    db.session.commit()
    if request.method == 'POST':
        return('TASK EDIT RECIEVED')

@app.route("/addCard", methods=["GET","POST"])
def addCard():
    title = request.form['title']
    corder = request.form['corder']
    card  = cards(title, corder)
    db.session.add(card)
    db.session.commit()
    if request.method == 'POST':
        return('CARD ADDITION RECIEVED')

@app.route("/addTask", methods=["GET","POST"])
def addTask():
    body = request.form['body']
    cid = request.form['cid']
    toder = request.form['torder']
    task  = tasks(body, cid, torder)
    db.session.add(task)
    db.session.commit()
    if request.method == 'POST':
        return('TASK ADDITION RECIEVED')

@app.route("/td", methods=["GET", "POST"])
def td():
    print(td)
    return ('td')

if __name__ == '__main__':
    app.run()