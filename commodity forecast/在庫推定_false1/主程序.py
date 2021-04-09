from 数据池 import Pond
import 数据变换 as Change
from 数据拟合 import Poly


class Guss:
    def __init__(self):
        self.pond = Pond(pond_size=8)  # 初始化数据池
        self.poly = Poly(mode='ave')  # 初始化拟合

    def fit(self, data):
        self.pond.append(data)             # 数据池
        data_x, data_y = self.pond.get()    #
        data_x = Change.data_filter(data_x, mode='kal')
        data_x = Change.data_change(data_x)  #
        self.poly.fit(data_x, data_y)

    def predict(self, data):
        data = Change.data_filter(data, mode='kal')  # 数据清洗-过滤
        print(data)
        data = Change.data_change(data)[-3:]  # 数据变换
        ret = self.poly.predict(data, mode='o')  # 估算
        return ret
