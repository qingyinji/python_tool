from 在庫推定.文件读取 import File
import 在庫推定.装饰器 as Wrapper
from 在庫推定.主程序 import Guss
import numpy as np

目录 = 'C:/Users/liang-jiashun/Desktop/库存感知测试结果汇总_最终'


@Wrapper.use_time(mode='s')
@Wrapper.自动评价(目录, 'C:/Users/liang-jiashun/Desktop/Excel模板/九宫格评价.xlsx', enable=False)
@Wrapper.列表循环(目录, enable_createFile=False)
def main(basic, path_train):
    print(path_train[1:])
    res = []
    file = File(path_train, basic)

    guss = Guss()

    for i in range(len(file.a)):
        guss.fit([file.a[i], file.b[i], file.c[i]])

    # a = [547, 556, 550]
    # b = [412, 413, 438]
    # c = [426, 427, 409]
    # res = guss.predict([a, b, c])
    # print(res)
    temp = file.pop()
    while temp is not None:
        result = []
        for _ in np.array(temp).T:
            ret = get_data_test(_[0], _[1], _[2])
            if len(ret) < 3:                                # 从第三次贩卖估算
                continue

            ret = guss.predict(ret)

            result.append(ret)
        get_data_test(0)

        guss.fit(temp)

        temp = file.pop()
        res.append(result)
        print(result)
        # output(basic + '/test/test_' + path_train[1:], result)
    return res

@Wrapper.cache_data
def get_data_test(*args):
    return list(args)


@Wrapper.output
def output(path, result):
    return path, result


if __name__ == '__main__':
    main()
