from flask import Flask, request, session
from flask.views import MethodView


app = Flask(__name__)


def get_db():
    client = MongoClient('mongodb://mongo:27017/')
    return client.flask_desk_database


def get_models_coll():
    return get_db()['model_collection']


class ModelAPI(MethodView):
    
    def post(self):
        return "Foo2"

app.add_url_rule('/models', view_func=ModelAPI.as_view('models'))


@app.route("/")
def hello():
    return """
Possible endpoints
- /models
"""


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
