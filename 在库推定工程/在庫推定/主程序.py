import 在庫推定.装饰器 as Wrapper
from 在庫推定.数据池 import Pond
import 在庫推定.数据变换 as Change
from 在庫推定.数据拟合 import Poly
from copy import deepcopy

from Excel.文件读取 import File
import Excel.装饰器 as Wr

目录 = 'C:/Users/liang-jiashun/Desktop/库存感知测试结果汇总_最终'


@Wr.use_time(mode='s')
@Wr.自动评价(目录, 'C:/Users/liang-jiashun/Desktop/Excel模板/九宫格评价.xlsx', enable=True)
@Wr.列表循环(目录)
def main(basic, path_train):
    print(path_train[1:])
    res = []
    file = File(path_train, basic)
    guss = Guess()

    for i in range(len(file.a)):
        for j in range(len(file.a[i])):
            guss.fit([file.a[i][j], file.b[i][j], file.c[i][j]])
        guss.fit([0, 0, 0])

    for i in range(1, len(file.a)):
        temp = []
        for j in range(len(file.a[i])):
            p = guss.predict([file.a[i][j], file.b[i][j], file.c[i][j]])
            if p is not None:
                temp.append(deepcopy(p))
        res.append(deepcopy(temp))
        # output(basic + '/test/test_' + path_train[1:], temp)
        temp.clear()
        guss.predict([0, 0, 0])

    return res


@Wr.output
def output(path, result):
    return path, result


class Guess:
    def __init__(self):
        self.pond = Pond(pond_size=8)  # 初始化数据池
        self.poly = Poly(pond=self.pond, mode='ave')  # 初始化拟合

    @Wrapper.cache_fit
    def fit(self,  x_time):
        x_timeA = Change.data_filter(x_time[0], mode='kal')
        x_timeB = Change.data_filter(x_time[1], mode='kal')
        x_timeC = Change.data_filter(x_time[2], mode='kal')
        # self.__pond_update(self.pond, self.poly, x_time)
        self.__pond_update(self.pond, self.poly, x_timeA, x_timeB, x_timeC)

    # @Wrapper.cache_pre
    # def predict(self, x_time, last=False):
    #     if len(x_time) < 3:                                # 从第三次贩卖估算
    #         return None
    #     if last:
    #         self.__pond_update(self.pond, self.poly, x_time)
    #         return
    #     x_time = Change.data_filter(x_time, mode='kal')[-3:]        # 数据清洗-过滤
    #     res = self.poly.predict(x_time, mode='o')   # 估算
    #     return res
    @Wrapper.cache_pre
    def predict(self, x_timeA, x_timeB, x_timeC, last=False):
        if len(x_timeA) < 3:  # 从第三次贩卖估算
            return None
        if last:
            self.__pond_update(self.pond, self.poly, x_timeA, x_timeB, x_timeC)
            return
        x_timeA = Change.data_filter(x_timeA, mode='kal')
        x_timeB = Change.data_filter(x_timeB, mode='kal')
        x_timeC = Change.data_filter(x_timeC, mode='kal')
        x_time = Change.data_change(x_timeA, x_timeB, x_timeC)
        res = self.poly.predict(x_time[-3:], mode='o')  # 估算
        return res

    # @staticmethod
    # def __pond_update(pond, poly, x_time):
    #     x_time.reverse()
    #     pond.append(x_time)                                # 数据池
    #     poly.fit()
    #     return

    @staticmethod
    def __pond_update(pond, poly, x_timeA, x_timeB, x_timeC):
        x_timeA.reverse()
        x_timeB.reverse()
        x_timeC.reverse()
        # x_time = Change.data_change(x_timeA, x_timeB, x_timeC)
        pond.append(x_timeA, x_timeB, x_timeC)  # 数据池
        poly.fit()
        return


if __name__ == '__main__':
    main()
