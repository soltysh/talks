import os

from flask import Flask
from flask_restful import Resource, Api
from flask.ext.restful.utils import cors

from db import Redis

app = Flask(__name__)
api = Api(app)
api.decorators = [cors.crossdomain(
    origin="*", headers=['accept', 'Content-Type'],
    methods=['HEAD', 'OPTIONS', 'GET', 'PUT', 'POST', 'DELETE'])]

class BlastVideo(Resource):

    def __init__(self):
        if 'BLAST_VIDEO_DB_SERVICE_HOST' in os.environ:
            self._db = Redis(os.environ['BLAST_VIDEO_DB_SERVICE_HOST'], \
                os.environ['BLAST_VIDEO_DB_SERVICE_PORT'])
        else:
            self._db = Redis('localhost', '6379')

    def get(self, tag):
        items = []
        for obj in self._db.get(tag):
            items.append({'url': obj.decode('utf-8')})
        return items


api.add_resource(BlastVideo, '/blast/api/v1.0/video/<string:tag>')

if __name__ == '__main__':
    app.run(debug=os.getenv('BLAST_DEBUG')=='True')
