from DataPond import Pond
from DataChange import Change
from DataPoly import Poly
from MysqlApl import DB
from math import exp
list_max = 20


class StockCal:
    def __init__(self, stockId):
        def __init__(self, stockId):
            with DB() as db:
                res = db.read_cache(stockId)
            self.poly = Poly(res)
            self.pond = Pond()
            self.change = Change()
            self.id = stockId

    def update(self, x_num, y_time):
        self.poly.fit(x_num, y_time)

    def predict(self):
        with DB() as db:
            sql = "SELECT id FROM data\
                                WHERE name = {} AND a = 0".format(self.stock)
            res_id = db.read(sql)
            size = res_id[1]['id'] - res_id[0]['id'] - 1

            for i in range(1, len(res_id) - 1):
                sql = "SELECT id, a, b, c FROM data\
                                    WHERE id > {} AND id < {}".format(res_id[i]['id'], res_id[i+1]['id'])
                res = db.read(sql)

                idd = [res[i]['id'] for i in range(len(res))]
                time_a = [res[i]['a'] for i in range(len(res))]
                time_b = [res[i]['b'] for i in range(len(res))]
                time_c = [res[i]['c'] for i in range(len(res))]

                y_time = self.change.data_change(time_a, time_b, time_c)
                y_time = self.change.filter(y_time)

                x_num = list(range(len(res), len(res) - size, -1))[2:]

                xx = len(idd) - len(y_time)
                for j, y in enumerate(y_time):
                    temp = (y - self.poly.b) / self.poly.k
                    res = min(self.pond.table, key=lambda x:abs(x - temp))
                    stock_pre = int(exp(res))
                    sql = "UPDATE data SET pre={}\
                                WHERE id={}".format(stock_pre, idd[j + xx])
                    db.read(sql)
                for j in range(xx):
                    sql = "UPDATE data SET pre={}\
                                WHERE id={}".format(0, idd[j])
                    db.read(sql)

                self.change.data_adjust(y_time)
                self.update(x_num, y_time)
