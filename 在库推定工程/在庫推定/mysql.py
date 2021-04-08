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

    def write(self, data):
        sql = "INSERT INTO {}({}) VALUES ('%s')".format('data', 'a') % data
        self.cur.execute(sql)
        self.conn.commit()

    def read(self):
        sql = "SELECT * FROM {}".format('data')
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results[0]['a']


if __name__ == '__main__':
    test = [1, 2, 3, 4, 5, 6, 7]
    with DB() as db:
        db.write(str(test))
        a = eval(db.read())
        print(a[2:])
