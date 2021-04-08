from 文件读取 import File
import 装饰器 as Wrapper
import numpy as np
import copy
from StockCalculation import StockCal

目录 = 'C:/Users/liang-jiashun/Desktop/库存感知测试结果汇总_最终'


@Wrapper.use_time(mode='s')
@Wrapper.自动评价(目录, 'C:/Users/liang-jiashun/Desktop/Excel模板/九宫格评价.xlsx', enable=True)
@Wrapper.列表循环(目录)
def main(basic, path_train):
    print(path_train[1:])
    res = []

    file = File(path_train, basic)
    stock_cal = StockCal()

    for i in range(len(file.a)):
        stock_cal.fit([file.a[i], file.b[i], file.c[i]])
        break
    temp = file.pop()
    temp[0].append(0)
    temp[1].append(0)
    temp[2].append(0)

    while temp is not None:
        result = []
        for _ in np.array(temp).T:

            cal = stock_cal.predict(_.tolist())
            if cal is not None:
                result.append(copy.deepcopy(cal))

        temp[0].pop(-1)
        temp[1].pop(-1)
        temp[2].pop(-1)
        stock_cal.fit(temp)

        temp = file.pop()
        res.append(result)
        print(result)
        # output(basic + '/test/test_' + path_train[1:], result)
    return res


@Wrapper.output
def output(path, result):
    return path, result


if __name__ == '__main__':
    main()
