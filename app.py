import os
import requests
import operator
import re
import nltk
import json
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job
#from worker import conn
import collections

app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

#q = Queue(connection=conn)
from models import *

@app.route("/", methods=["GET", "POST"])
def index():
    return ("hello world")