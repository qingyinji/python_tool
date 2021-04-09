import pymysql


class DB:
    def __init__(self, host='localhost', port=3306, db_='test', user='wj',
                 passwd='', charset='utf8'):
        self.db = db_
        self.conn = pymysql.connect(host=host, port=port, db=db_, user=user, passwd=passwd, charset=charset)
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def read(self,sql):
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results

    def write(self, sql):
        self.cur.execute(sql)

    def read_cache(self, data_id):
        sql = "SELECT cache FROM data_id\
                            WHERE data_id = {}".format(data_id)
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results[0]['cache']
