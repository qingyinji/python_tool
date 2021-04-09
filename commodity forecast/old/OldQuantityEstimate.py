import ReadFile
import WriteExcel
import copy
from scipy.optimize import leastsq

import numpy as np
import math

path = "E:/input1.log"
path1 = "E:/input2.log"
# -----------------------------------------------------------------------------------------------------


class Object:
    path_train = ''
    data_train = []
    data_train_fli = []

    path_test = ''
    data_test = []

    a = 0
    b = 0

    def __init__(self, path_train, path_test):
        self.path_train = path_train
        self.path_test = path_test
# -----------------------------------------------------------------------------------------------------


def calc_avg(data):
    if len(data) == 3:
        return data[0]*0.2 + data[1]*0.3 + data[2]*0.6
    else:
        return sum(data)/len(data)


# 需要拟合的函数func :指定函数的形状 k= 0.42116973935 b= -8.28830260655
def func(p, xx):
    k, bb = p
    return k * xx + bb


# 偏差函数：x,y都是列表:这里的x,y更上面的Xi,Yi中是一一对应的
def error(p, xx, yy):
    return func(p, xx) - yy


def adjust_data(data):
    for _ in range(2):
        if data[_] > 1000:
            data[_] = 1000
        elif data[_] < 400:
            data[_] = 400

    for _ in range(2, len(data)):
        start = 0
        if data[_] > 1000 or data[_] < 400:
            for _ in range(i + 1, len(data)):
                if 400 < data[i] < 1000:
                    start = _
                    break
            if start != 0:
                data[i] = (data[i - 1] + data[start]) / 2
            else:
                if data[i] > 1000:
                    data[i] = 1000
                elif data[i] < 400:
                    data[i] = 400


def calc_func(data):
    xx = []
    for _ in range(len(data), 0, -1):
        xx.append(math.log(_))
    yyy = np.array(data)
    xxx = np.array(xx)

    # k,b的初始值，可以任意设定,经过几次试验，发现p0的值会影响cost的值：Para[1]
    pp0 = [-10, 700]
    # 把error函数中除了p0以外的参数打包到args中(使用要求)
    paraa = leastsq(error, pp0, args=(xxx, yyy))
    # 读取结果
    if this.a == 0 or this.b == 0:
        this.a, this.b = paraa[0]
    else:
        aa, bb = paraa[0]
        this.a = this.a * 0.5 + aa * 0.5
        this.b = this.b * 0.5 + bb * 0.5


this = Object(path, path1)
ReadFile.readfile(this.path_train, this.data_train, 1)  # 读取训练数据
ReadFile.readfile(this.path_test, this.data_test, 1)  # 读取测试数据

for temp in this.data_train:                      # 舍弃第一个数据
    temp.pop(0)
for temp in this.data_test:
    temp.pop(0)

for temp in this.data_train:                                        # 消除数据异常值
    adjust_data(temp)

for temp in this.data_train:
    fli_temp = []
    # fli_temp.append(copy.deepcopy(temp[0]))
    # fli_temp.append(copy.deepcopy((temp[0]+temp[1])/2))
    for i in range(2, len(temp)):
        fli_temp.append((temp[i-2]*0.2+temp[i-1]*0.3+temp[i]*0.5))
    this.data_train_fli.append(copy.deepcopy(fli_temp))
    fli_temp.clear()

for _ in this.data_train_fli:
    calc_func(_)

result = []
WriteExcel.initexcel()

for temp in this.data_test:
    for i in range(2, len(temp)):
        if temp[i] > 1000:
            temp[i] = 1000
        elif temp[i] < 400:
            temp[i] = 400
        judged_data = (temp[i-2]*0.2+temp[i-1]*0.3+temp[i]*0.5)
        numerator = judged_data - this.b
        log_x = numerator / this.a

        result_num = 1
        for ii in range(15, 0, -1):
            if math.log(ii) <= log_x:
                break
        if ii == 15:
            result_num = 15
        elif ii >= 0:
            diff1 = log_x - math.log(ii)
            diff2 = math.log(ii+1) - log_x
            if diff1 <= diff2:
                result_num = ii - 1
            else:
                result_num = ii
            if result_num <= 0:
                result_num = 1

        result.append(result_num)
    print('数量估计：', result)
    WriteExcel.writeexcel(result)      # 将结果写入Excel中
# ----------------------------------------------------------------------------------------------------------------------
    adjust_data(temp)
    calc_func(temp)

    result.clear()

