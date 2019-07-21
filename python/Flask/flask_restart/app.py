# -*- encoding: utf-8 -*-
from pprint import pprint
from flask import Flask, g

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello"
