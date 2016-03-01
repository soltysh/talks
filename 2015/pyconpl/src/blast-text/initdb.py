import os

from pymongo import MongoClient

def initdb(username, password, host, port):
    client = MongoClient('mongodb://{}:{}@{}:{}/blast_text'.format(username, password, host, port))
    collection = client.blast_text.text
    if collection.count() == 0:
        collection.insert_many([
            {'text': 'openshift is sooo cool', 'url': 'http://www.example.com/cool'},
            {'text': 'openshift is awesome', 'url': 'http://www.example.com/awesome'},
            {'text': 'soltysh is very handsome', 'url': 'http://www.example.com/handsome'},
            {'text': 'kittens are soo cute', 'url': 'http://www.example.com/cute'},
            {'text': 'programming in python', 'url': 'http://www.python.org/'},
            {'text': 'programming in go', 'url': 'http://www.golang.org/'},
        ])

if __name__ == '__main__':
    if 'BLAST_TEXT_DB_SERVICE_HOST' in os.environ:
        initdb(os.environ['MONGODB_USER'], \
            os.environ['MONGODB_PASSWORD'], \
            os.environ['BLAST_TEXT_DB_SERVICE_HOST'], \
            os.environ['BLAST_TEXT_DB_SERVICE_PORT'])
    else:
        initdb('user', 'password', 'localhost', '27017')
