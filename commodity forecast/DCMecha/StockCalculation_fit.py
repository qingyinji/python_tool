from DataPond import Pond
from DataChange import Change
from DataPoly import Poly
from MysqlApl import DB
list_max = 20


def main(data_id):
    stock_cal = StockCalFit(data_id)
    stock_cal.fit()
    stock_cal.finish()


class StockCalFit:
    def __init__(self, stockId):
        with DB() as db:
            res = db.read_cache(stockId)
        self.poly = Poly(res)
        self.pond = Pond()
        self.change = Change()
        self.id = stockId

    def fit(self):
        with DB() as db:
            sql = "SELECT time FROM data_update\
                    WHERE data_id = {}".format(self.id)
            time_list = db.read(sql)
            if len(time_list) > list_max:
                time_list = time_list[len(time_list)-list_max:]

            for i in range(len(time_list)):
                try:
                    sql = "SELECT a, b, c FROM data WHERE data_id = {} " \
                          "AND unix_timestamp(time) > unix_timestamp('{}')" \
                          "AND unix_timestamp(time) < unix_timestamp('{}')"\
                            .format(self.id, time_list[i]['time'], time_list[i+1]['time'])
                except IndexError:
                    sql = "SELECT a, b, c FROM data WHERE data_id = {} " \
                          "AND unix_timestamp(time) > unix_timestamp('{}')" \
                        .format(self.id, time_list[i]['time'])

                res = db.read(sql)
                if len(res) == 0:
                    continue

                time_a = [res[i]['a'] for i in range(len(res))]
                time_b = [res[i]['b'] for i in range(len(res))]
                time_c = [res[i]['c'] for i in range(len(res))]

                y_time = self.change.data_change(time_a, time_b, time_c)
                y_time = self.change.filter(y_time)
                x_num = list(range(len(res), 0, -1))[2:]

                self.__update(x_num, y_time)

    def finish(self):
        sql = "UPDATE data_id SET cache = '{}' WHERE data_id = {}"\
            .format(str([self.poly.k, self.poly.b]), self.id)
        with DB() as db:
            db.write(sql)

    def __update(self, x_num, y_time):
        self.poly.fit(x_num, y_time)