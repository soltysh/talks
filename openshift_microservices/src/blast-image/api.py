import os

from flask import Flask
from flask_restful import Resource, Api
from flask.ext.restful.utils import cors

from db import PostgreSQL

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(
    origin="*", headers=['accept', 'Content-Type'],
    methods=['HEAD', 'OPTIONS', 'GET', 'PUT', 'POST', 'DELETE'])]

class BlastImage(Resource):

    def __init__(self):
        self._db = PostgreSQL('user', 'password', 'localhost', '5432')

    def get(self, tag):
        items = []
        for obj in self._db.get(tag):
            items.append({'tag': obj['tag'], 'image': obj['image']})
        return items


api.add_resource(BlastImage, '/blast/api/v1.0/image/<string:tag>')

if __name__ == '__main__':
    app.run(debug=os.getenv('BLAST_DEBUG')=='True')
