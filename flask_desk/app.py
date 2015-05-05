#coding=utf-8

import copy
import datetime
import logging
from bson import ObjectId, json_util
import json
from flask import Flask, request
from flask.views import MethodView
from utils import output_json, get_schema_coll, get_ticket_coll


app = Flask(__name__)


class SchemaResource(MethodView):

    def validate_post(self, data):
        mandatory_fields = ['name', 'status_list']
        for i in mandatory_fields:
            if i not in data:
                raise ValueError("'%s' not found" % i)

    def clear_data(self, data):
        preserve = ['name', 'status_list', 'meta']
        my_keys = data.keys()
        my_keys = list(my_keys)
        for i in my_keys:
            if i in preserve:
                preserve.remove(i)
                continue
            data.pop(i)
        return data

    def post(self):
        data = request.get_json(True)
        self.validate_post(data)
        data = self.clear_data(data)

        schema_coll = get_schema_coll()
        ret = schema_coll.insert_one(data)

        return output_json({'success': True}, 200)

    def _get_one(self, _id):
        logging.debug("Getting just one: %s " % _id)
        _id = ObjectId(_id)
        coll = get_schema_coll()
        ret = coll.find_one({"_id": _id})
        return output_json(ret, 200)

    def get(self, _id=None):
        if _id is not None:
            return self._get_one(_id)
        schema_coll = get_schema_coll()
        ret = schema_coll.find()
        return output_json(ret, 200)


schema_resource_view = SchemaResource.as_view('schema_res')
app.add_url_rule('/schema', view_func=schema_resource_view)
app.add_url_rule('/schema/<string:_id>',
                 view_func=schema_resource_view,
                 methods=['GET', 'DELETE'])


class TicketResource(MethodView):

    def pub(self, new_ticket, old_ticket=None):
        logging.debug("trying to publish the history")
        try:
            import redis
            r = redis.StrictRedis(host='redis', port=6379, db=0)
            ret = r.publish("ticket-data", json_util.dumps({
                'new_ticket': new_ticket,
                'old_ticket': old_ticket
            }))
            logging.debug(ret)
        except Exception as e:
            logging.error("error while trying to pub on redis")
            logging.error(e)

    def post(self):
        ret = None
        data = request.get_json(True)
        expected = ['schema', 'data', 'status']
        for i in expected:
            if i not in data.keys():
                raise ValueError("%s not found" % i)

        # get schema
        schema_id = ObjectId(data["schema"])
        schema_coll = get_schema_coll()
        schema = schema_coll.find_one({"_id": schema_id})
        logging.debug(schema)
        if not schema:
            raise Exception("schema '%s' not found" % data['schema'])


        # check status
        if data['status'] not in schema['status_list']:
            msg = "status '%s'not found on schema '%s'. Expected: '%s'"
            msg = msg % (data['status'],
                         schema['name'],
                         schema['status_list'])
            raise Exception(msg)

        data['open_date'] = datetime.datetime.now()
        logging.debug(data)

        collection = get_ticket_coll()
        collection.insert_one(data)
        self.pub(data)
        return output_json({'success': True}, 200)

    def put(self, _id):
        logging.debug("Getting just one: %s " % _id)
        my_ticket = self._get_one(_id)
        old_ticket = copy.deepcopy(my_ticket)
        _id = my_ticket['_id']
        data = request.get_json(True)

        # todo :: change signal
        if 'data' in data:
            my_ticket['data'].update(data['data'])
    
        if 'status' in data:
            my_ticket['status'] = data['status']

        coll = get_ticket_coll()
        coll.replace_one({"_id": _id}, my_ticket)

        self.pub(my_ticket, old_ticket)
        return output_json(my_ticket, 200)

    def _get_one(self, _id):
        logging.debug("Getting just one: %s " % _id)
        _id = ObjectId(_id)
        coll = get_ticket_coll()
        ret = coll.find_one({"_id": _id})
        ret['schema_url'] = "/schema/%s" % ret['schema']
        return ret

    def get(self, _id=None):
        if _id is not None:
            ret = self._get_one(_id)
        else:
            collection = get_ticket_coll()
            ret = collection.find()
        return output_json(ret, 200)

ticket_resource_view = TicketResource.as_view('ticket_resource')
app.add_url_rule('/ticket',
                 view_func=ticket_resource_view,
                 methods=['GET', 'POST'])
app.add_url_rule('/ticket/<string:_id>',
                 view_func=ticket_resource_view,
                 methods=['PUT', 'GET', 'DELETE'])


@app.route("/")
def hello():
    return """
Possible endpoints
- /schema
- /ticket
"""
