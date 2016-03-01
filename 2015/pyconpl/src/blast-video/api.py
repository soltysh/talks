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

class BlastVideo(Resource):

    def __init__(self):
        if 'BLAST_VIDEO_DB_SERVICE_HOST' in os.environ:
            self._db = Mongo(os.environ['MONGODB_USER'], \
                os.environ['MONGODB_PASSWORD'], \
                os.environ['BLAST_VIDEO_DB_SERVICE_HOST'], \
                os.environ['BLAST_VIDEO_DB_SERVICE_PORT'])
        else:
            self._db = Mongo('user', 'password', 'localhost', '27017')

    def get(self, tag):
        items = []
        for obj in self._db.get(tag):
            items.append({'id': str(obj['_id']), 'url': obj['url'], 'title': obj['title']})
        return items


api.add_resource(BlastVideo, '/blast/api/v1.0/video/<string:tag>')

if __name__ == '__main__':
    app.run(debug=os.getenv('BLAST_DEBUG')=='True')
