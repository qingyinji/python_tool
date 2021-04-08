import pymysql
from 获取数据 import get_data
import 装饰器 as Wrapper
目录 = 'C:\\Users\\Nao KeTeng\\OneDrive\\桌面\\data'


@Wrapper.use_time(mode='s')
@Wrapper.列表循环(目录, enable_createFile=False)
def main(basic, path_train):
    print(path_train[1:])
    file = get_data(basic + path_train)
    with DB() as db:
        for i in range(len(file.data1)):
            db.write(file.package_mess[0][0], file.data1[i], file.data2[i], file.data3[i], file.data4[i])

# def main():
#     with DB() as db:
#         goods = db.read_id()
#         for i in goods:
#             data = db.read_data(i['name'])
#             break


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

    def read_id(self):
        sql = "SELECT * FROM good_id"
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results

    def read_data(self, name):
        sql = "SELECT a, b, c FROM data \
                WHERE name = {}".format('\'' + name + '\'')
        self.cur.execute(sql)
        results = self.cur.fetchall()
        return results

    def write(self, name, a, b, c, d):
        sql = "INSERT INTO data(name, a, b, c, d)\
                VALUES (%s, %s, %s, %s, %s)" %\
              ('\'' + name + '\'', a, b, c, d)
        self.cur.execute(sql)

    def write1(self, name):
        sql = "INSERT INTO good_id(name)\
                VALUES (%s)" %\
              ('\'' + name + '\'')
        self.cur.execute(sql)


if __name__ == '__main__':
    main()
