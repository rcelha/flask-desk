#coding=utf-8

import logging
from bson import ObjectId
from flask import Flask, request
from flask.views import MethodView
from utils import output_json, get_schema_coll


app = Flask("flask-desk")


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

