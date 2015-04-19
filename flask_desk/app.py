#coding=utf-8

import datetime
import logging
from bson import ObjectId
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

    def get(self):
        schema_coll = get_schema_coll()
        ret = schema_coll.find()
        return output_json(ret, 200)

app.add_url_rule('/schema', view_func=SchemaResource.as_view('schema_res'))


class TicketResource(MethodView):


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
        return output_json({'success': True}, 200)

    def _get_one(self, _id):
        logging.debug("Getting just one: %s " % _id)
        _id = ObjectId(_id)
        coll = get_ticket_coll()
        ret = coll.find_one({"_id": _id})
        return output_json(ret, 200)

    def get(self, _id=None):
        if _id is not None:
            return self._get_one(_id)
        collection = get_ticket_coll()
        ret = collection.find()
        return output_json(ret, 200)

ticket_resource_view = TicketResource.as_view('ticket_resource')

app.add_url_rule('/ticket',
                 view_func=ticket_resource_view,
                 methods=['GET', 'POST'])
app.add_url_rule('/ticket/<string:_id>',
                 view_func=ticket_resource_view,
                 methods=['GET', 'DELETE'])


@app.route("/")
def hello():
    return """
Possible endpoints
- /schema
- /ticket
"""


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    app.run(host="0.0.0.0", debug=True)
