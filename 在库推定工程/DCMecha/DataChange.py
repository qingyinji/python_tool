from numpy import array
from copy import deepcopy
StockCal_RANGE_MIN = 400
StockCal_RANGE_MAX = 1000


class Change:
    @staticmethod
    def data_change(a, b, c):
        a = array(a)
        b = array(b)
        c = array(c)
        ret = a + b - c
        return ret.tolist()

    @staticmethod
    def filter(data):
        window = [0.2, 0.3, 0.6]
        data_temp = []
        for i in range(len(data) - 2):
            data_temp.append(window[0]*data[i] + window[1]*data[i+1] + window[2]*data[i+2])
        return deepcopy(data_temp)

    @staticmethod
    def data_adjust(data):
        def search_normal_data(data_):
            for _ in data_:
                if StockCal_RANGE_MIN <= _ <= StockCal_RANGE_MAX:
                    return _
            return None

        for i, temp in enumerate(data):
            if StockCal_RANGE_MIN <= temp <= StockCal_RANGE_MAX:
                continue
            try:
                nor = search_normal_data(data[i+1:])
                if nor is None:
                    if temp < StockCal_RANGE_MIN:
                        data[i] = StockCal_RANGE_MIN
                    else:
                        data[i] = StockCal_RANGE_MAX
                else:
                    data[i] = (data[i-1] + nor) / 2
            except IndexError:
                if temp < StockCal_RANGE_MIN:
                    data[i] = StockCal_RANGE_MIN
                else:
                    data[i] = StockCal_RANGE_MAX
        return data
