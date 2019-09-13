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

#q = Queue(connection=conn)
from models import *
# cardtest = cards('cardtesttitle')
# db.session.add(cardtest)
# db.session.commit()
# tasktest = tasks(1,"taskbodytest", 1)
# db.session.add(tasktest)
# db.session.commit()
# cd=cards.query.all()
# td=tasks.query.all()
# print(cd)
# print(td)
# print('tasks')
# for t in td:
    # print (t.body,t.id)
    # db.session.delete(t)
    # db.session.commit()
# print('cards')
# for c in cd:
    # print (c.title,c.id)
    # db.session.delete(c)
    # db.session.commit()
# cd=cards.query.all()
# td=tasks.query.all()
# print(cd)
# print(td)
@app.route("/", methods=["GET", "POST"])
def index():
    return ("hello world")

@app.route("/boardData", methods=["GET", "POST"])
def bd():
    # cardDict={}
    # taskDict={}
    # cardDict['cards']=[]
    board={}
    board['cards']=[]
    board['tasks']=[]
    x=cards.query.all()
    for c in x:
        board['cards'].append([c.id, c.title, c.num_tasks, c.created])
    y=tasks.query.all()
    for t in y:
        board['tasks'].append([t.id, t.cid, t.body, t.created, t.torder])
    # return jsonify(x)
    # print('jsonify')
    # print (jsonify(cardDict))
    return(jsonify(board))

@app.route("/cd", methods=["GET", "POST"])
def cd():
    print("IN CD")
    cardDict={}
    cardDict['cards']=[]
    # print(cd)
    x=cards.query.all()
    for c in x:
        cardDict['cards'].append([c.title, c.created])
        # print(cardDict[c.id])
    # return jsonify(x)
    # print('jsonify')
    # print (jsonify(cardDict))
    return(jsonify(cardDict))

@app.route("/td", methods=["GET", "POST"])
def td():
    print(td)
    return ('td')

if __name__ == '__main__':
    app.run()