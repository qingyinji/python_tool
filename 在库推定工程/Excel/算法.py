import 装饰器 as Wrapper
from 数据池 import Pond
import 数据变换 as Change
from 数据拟合 import Poly


class Guess:
    def __init__(self):
        self.pond = Pond(pond_size=8)  # 初始化数据池
        self.poly = Poly(mode='ave')  # 初始化拟合

    def fit(self, y_number, x_time):
        self.__pond_update(self.pond, self.poly, [x_time[0], x_time[1], x_time[2]])

    def predict(self, x_time):
        ret = self.__get_data(x_time[0], x_time[1], x_time[2])
        if len(ret) < 3:                                # 从第三次贩卖估算
            return None
        ret = Change.data_filter(ret, mode='kal')        # 数据清洗-过滤
        ret = Change.data_change(ret)[-3:]              # 数据变换

        res = self.poly.predict(ret, mode='rnew')   # 估算
        self.__pond_update(self.pond, self.poly, x_time)
        return res

    @staticmethod
    def __pond_update(pond, poly, x):
        pond.append(x)                                # 数据池
        data_x, data_y = pond.get()  #
        Change.data_filter(data_x, mode='kal')
        data_x = Change.data_change(data_x)  #
        poly.fit(data_x, data_y)
        return

    @Wrapper.cache_data
    def __get_data(self, *args):
        return list(args)
