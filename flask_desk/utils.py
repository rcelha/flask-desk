#coding=utf-8

from flask import make_response
from pymongo import MongoClient
from bson.json_util import dumps

def output_json(obj, code, headers=None):
    resp = make_response(dumps(obj), code)
    resp.headers.extend(headers or {})
    return resp

def get_db():
    client = MongoClient('mongodb://mongo:27017/')
    return client.flask_desk_database

def get_schema_coll():
    return get_db()['schema_collection']

def get_ticket_coll():
    return get_db()['ticket_collection']
