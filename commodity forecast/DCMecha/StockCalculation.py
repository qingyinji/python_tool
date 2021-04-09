from DataPond import Pond
from DataChange import Change
from DataPoly import Poly
from MysqlApl import DB
from math import exp
list_max = 20
list_max_pre = 20


def main(data_id, flag):
    stock_cal = StockCal(data_id)
    if flag == 0:
        stock_cal.fit()
    else:
        stock_cal.predict()
    stock_cal.finish()


class StockCal:
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

                time_a, time_b, time_c = self.__abc_to_list(res)

                y_time = self.change.data_change(time_a, time_b, time_c)
                y_time = self.change.filter(y_time)
                x_num = list(range(len(res), 0, -1))[2:]

                self.__update(x_num, y_time)

    def predict(self):
        with DB() as db:
            sql = "SELECT time FROM data_update\
                    WHERE data_id = {}".format(self.id)
            time_list = db.read(sql)
            if len(time_list) > list_max:
                time_list = time_list[len(time_list) - list_max:]

            for i in range(len(time_list)):
                try:
                    sql = "SELECT time, a, b, c FROM data WHERE data_id = {} " \
                          "AND unix_timestamp(time) > unix_timestamp('{}')" \
                          "AND unix_timestamp(time) < unix_timestamp('{}')" \
                        .format(self.id, time_list[i]['time'], time_list[i + 1]['time'])
                except IndexError:
                    sql = "SELECT time, a, b, c FROM data WHERE data_id = {} " \
                          "AND unix_timestamp(time) > unix_timestamp('{}')" \
                        .format(self.id, time_list[i]['time'])

                res = db.read(sql)
                if len(res) == 0:
                    continue

                time_a, time_b, time_c = self.__abc_to_list(res)
                time_data = [res[i]['time'] for i in range(len(res))]

                y_time = self.change.data_change(time_a, time_b, time_c)
                y_time = self.change.filter(y_time)

                x_num = list(range(len(res), 0, -1))[2:]

                print(len(time_data))
                print(len(y_time))
                for j, y in enumerate(y_time):
                    temp = (y - self.poly.b) / self.poly.k
                    res = min(self.pond.table, key=lambda x: abs(x - temp))
                    stock_pre = int(exp(res))
                    sql = "UPDATE data SET pre={}\
                                WHERE time='{}' AND data_id = {}".format(stock_pre, time_data[j+2], self.id)
                    db.read(sql)
                for j in range(2):
                    sql = "UPDATE data SET pre={}\
                                WHERE time='{}'".format(0, time_data[j])
                    db.read(sql)

                self.change.data_adjust(y_time)
                self.__update(x_num, y_time)

    def finish(self):
        sql = "UPDATE data_id SET cache = '{}' WHERE data_id = {}"\
            .format(str([self.poly.k, self.poly.b]), self.id)
        with DB() as db:
            db.write(sql)

    def __update(self, x_num, y_time):
        self.poly.fit(x_num, y_time)

    @staticmethod
    def __abc_to_list(res):
        time_a = [res[i]['a'] for i in range(len(res))]
        time_b = [res[i]['b'] for i in range(len(res))]
        time_c = [res[i]['c'] for i in range(len(res))]
        return time_a, time_b, time_c
