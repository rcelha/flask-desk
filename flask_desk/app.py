#coding=utf-8

from flask import Flask


app = Flask(__name__)

from schema_resource import *
from ticket_resource import *

@app.route("/")
def hello():
    return """
<h1>Possible endpoints </h1>
<ul>
    <li> /schema </li>
    <li> /ticket </li>
</ul>
"""
