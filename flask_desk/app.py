#coding=utf-8

from flask import Flask


app = Flask("flask-desk")

from schema_resource import *
from ticket_resource import *

@app.route("/")
def hello():
    return """
Possible endpoints
- /schema
- /ticket
"""
