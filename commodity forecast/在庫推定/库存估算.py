from 文件读取 import File
import 装饰器 as Wrapper
from 数据池 import Pond
import 数据变换 as Change
from 数据拟合 import Poly
import numpy as np

目录 = 'C:/Users/liang-jiashun/Desktop/库存感知测试结果汇总_最终'


@Wrapper.use_time(mode='s')
@Wrapper.自动评价(目录, 'C:/Users/liang-jiashun/Desktop/Excel模板/九宫格评价.xlsx', enable=True)
@Wrapper.列表循环(目录)
def main(basic, path_train):
    print(path_train[1:])
    res = []

    file = File(path_train, basic)
    pond = Pond(pond_size=8)                               # 初始化数据池
    poly = Poly(mode='ave')                                 # 初始化拟合

    for i in range(len(file.a)):
        pond_update(pond, poly, [file.a[i], file.b[i], file.c[i]])
        break

    temp = file.pop()
    while temp is not None:
        result = []
        for _ in np.array(temp).T:
            ret = get_data_test(_[0], _[1], _[2])
            if len(ret) < 3:                                # 从第三次贩卖估算
                continue

            ret = Change.data_filter(ret, mode='kal')        # 数据清洗-过滤
            ret = Change.data_change(ret)[-3:]              # 数据变换

            result.append(poly.predict(ret, mode='rnew'))   # 估算
        get_data_test(0)

        pond_update(pond, poly, temp)

        temp = file.pop()
        res.append(result)
        print(result)
        # print(poly.table)
        # import sg平滑滤波 as Sg
        # print(Sg.savgol(poly.table, 3, 2))
        output(basic + '/test/test_' + path_train[1:], result)

    return res


def pond_update(pond, poly, x):
    pond.append(x)                                # 数据池
    data_x, data_y = pond.get()  #
    Change.data_filter(data_x, mode='kal')
    data_x = Change.data_change(data_x)  #

    poly.fit(data_x, data_y)
    pass

    # from matplotlib import pyplot as plt
    # import sg平滑滤波 as sg
    # plt.plot(range(len(poly.table)), poly.table)
    # plt.plot(range(len(poly.table)), sg.savgol(poly.table, 3, 2))
    # plt.show()


@Wrapper.cache_data
def get_data_test(*args):
    return list(args)


@Wrapper.output
def output(path, result):
    return path, result


if __name__ == '__main__':
    main()
