import numpy as np
import math
import random
import ReadFile
import copy


def create_data(data_in, data_flag, number):
    path = "C:/Users/Nao KeTeng/OneDrive/桌面/input.log"
    data = []
    ReadFile.readfile(path, data)
    for _ in data:                      # 舍弃第一个数据
        _.pop(0)

    time = 3
    flag = 0
    polynomial = [0, 0, 0, 0]
    # aa:训练拟合权重
    aa = 0.8

    for temp in data:
        z1 = np.polyfit(list(range(len(temp), 0, -1)), temp, time)
        p1 = np.poly1d(z1)

        if (polynomial[0] + polynomial[1] + polynomial[2] + polynomial[3]) == 0:
            flag = 1
        else:
            flag = 0
        if flag != 1:
            for i in range(time + 1):
                polynomial[i] = (1 - aa) * p1[i] + aa * polynomial[i]
        else:
            for i in range(time + 1):
                polynomial[i] = p1[i] + polynomial[i]

    result = []
    for i in range(15, 0, -1):
        result_temp = polynomial[0]+(polynomial[1]*i)+(polynomial[2]*(i**2))+(polynomial[3]*(i**3))
        result.append(result_temp)

    if data_flag == 2:
        for i in range(number):
            start = random.randint(1, 10)
            translation = np.random.normal(0, 4)
            jj = 0
            data_temp = []
            for _ in result:
                _ += (math.cos(math.pi * (start+jj)) * abs(np.random.normal(0, 4))) + translation
                jj += 1
                data_temp.append(_)
            data_in.append(copy.deepcopy(data_temp))
            data_temp.clear()

    elif data_flag == 3:
        for i in range(int(number/len(data))):
            for one in data:
                data_temp = []
                for _ in one:
                    data_temp.append(_ + +np.random.normal(-5, 5))
                data_in.append(copy.deepcopy(data_temp))
                data_temp.clear()
