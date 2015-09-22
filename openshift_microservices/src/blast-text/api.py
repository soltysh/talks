import os

from flask import Flask
from flask_restful import Resource, Api
from flask.ext.restful.utils import cors

from db import Mongo

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(
    origin="*", headers=['accept', 'Content-Type'],
    methods=['HEAD', 'OPTIONS', 'GET', 'PUT', 'POST', 'DELETE'])]

class BlastText(Resource):

    def __init__(self):
        self._db = Mongo('user', 'password', 'localhost', '27017')

    def get(self, text):
        items = []
        for obj in self._db.get(text):
            items.append({'id': str(obj['_id']), 'url': obj['url'], 'text': obj['text']})
        return {'items': items}


api.add_resource(BlastText, '/blast/api/v1.0/text/<string:text>')

if __name__ == '__main__':
    app.run(debug=os.getenv('BLAST_DEBUG')=='True')
