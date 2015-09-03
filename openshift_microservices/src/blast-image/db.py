import psycopg2

class PostgreSQL():

    def __init__(self, username, password, host, port):
        self._conn = psycopg2.connect(user=username, password=password, \
            host=host, port=port, database='blast_image')


    def get(self, tag):
        result = []
        cur = self._conn.cursor()
        cur.execute("select tag, image from image where tag=%s", (tag, ))
        for rec in cur:
            result.append({'tag': rec[0], 'image': rec[1].tobytes()})
        cur.close()
        return result
