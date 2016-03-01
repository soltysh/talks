import os

from pymongo import MongoClient

def initdb(username, password, host, port):
    client = MongoClient('mongodb://{}:{}@{}:{}/blast_video'.format(username, password, host, port))
    collection = client.blast_video.video
    if collection.count() == 0:
        collection.insert_many([
            {'title': 'openshift', 'url': 'https://youtu.be/FAJsx1HxsuM?t=2279'},
            {'title': 'openshift', 'url': 'https://youtu.be/uocucZqg_0I'},
            {'title': 'openshift', 'url': 'https://youtu.be/nDg8NuchvAs'},
            {'title': 'pyconpl', 'url': 'https://youtu.be/T-ddE-aIX0k'},
            {'title': 'pyconpl', 'url': 'https://youtu.be/CNvjKrCbw2A'},
            {'title': 'pyconpl', 'url': 'https://youtu.be/-PisXGVe-lE'},
        ])

if __name__ == '__main__':
    if 'BLAST_VIDEO_DB_SERVICE_HOST' in os.environ:
        initdb(os.environ['MONGODB_USER'], \
            os.environ['MONGODB_PASSWORD'], \
            os.environ['BLAST_VIDEO_DB_SERVICE_HOST'], \
            os.environ['BLAST_VIDEO_DB_SERVICE_PORT'])
    else:
        initdb('user', 'password', 'localhost', '27017')

