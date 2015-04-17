#coding=utf-8

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
        data = request.get_json(True)
        expected = ['schema', 'data', 'status']
        for i in expected:
            if i not in data.keys():
                raise ValueError("%s not found" % i)

        schema_coll = get_schema_coll()
        ret = schema_coll.find_one({"_id": data['schema']})
        print(ret)


        return output_json({'success': True}, 200)

    def get(self):
        collection = get_ticket_coll()
        ret = collection.find()
        return output_json(ret, 200)

app.add_url_rule('/ticket', view_func=TicketResource.as_view('ticket_res'))


@app.route("/")
def hello():
    return """
Possible endpoints
- /schema
- /ticket
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
