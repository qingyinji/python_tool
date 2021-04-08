import numpy as np
import math
import 获取数据 as Get
import sg平滑滤波 as Sg
from copy import deepcopy


def main():
    this = Get.get_data("C:/Users/liang-jiashun/Desktop/0011.xlsx")
    a = log(this.data1)
    print(a)


def data_filter(data, mode='sg'):
    # data_ = data_errorDel(data_)                  # 启用后准确率大幅下降
    if mode == 'sg':
        data = Sg.savgol(data, 3, 2)

    elif mode == 'ave':
        window = [0.2, 0.3, 0.5]
        data[1] = (data[0] + data[1])/2
        for i in range(len(data[2:])):
            data[i+2] = data[i]*window[0] + data[i+1]*window[1] + data[i+2]*window[2]

    elif mode == 'kal':
        data = kalman(data)
        data = data.tolist()

    return data


# def data_change(x):
#     return x[0] + x[1] - x[2]
def data_change(a, b, c):
    ret = []
    for i in range(len(a)):
        temp = np.array(a[i]) + np.array(b[i]) + np.array(c[i])
        ret.append(deepcopy(temp.tolist()))
    return ret


def kalman(data):
    n_iter = len(data)
    sz = n_iter
    # Q = 8e-3            # 处理误差 down
    # R = 0.1 ** 2        # 估计误差 up
    Q = 9  # 处理误差 down
    R = 20  # 估计误差 up
    # 分配数组空间
    xhat = np.zeros(sz)
    P = np.zeros(sz)
    xhatminus = np.zeros(sz)
    Pminus = np.zeros(sz)
    K = np.zeros(sz)

    # xhat[0] = data[0]
    xhat[0] = 400
    P[0] = 1.0

    for k in range(1, n_iter):
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + Q

        K[k] = Pminus[k] / (Pminus[k] + R)
        xhat[k] = xhatminus[k] + K[k] * (data[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]

    return xhat


def data_errorDel(data):
    ret = []
    for temp in data.tolist():
        index = -1
        start = 3
        param = 0.9
        for _ in temp:
            index += 1
            if _ > 1000:
                if (index > 0) and (index < len(temp) - 1):
                    temp[index] = (temp[index - 1] + temp[index + 1]) / 2
                elif index == 0:
                    temp[index] = temp[index + 1]
                elif index == len(temp)-1:
                    temp[index] = temp[index - 1]
        y1 = 0
        for i in range(len(temp)-start):
            for j in range(start-1):
                y1 += abs(temp[j+i+1] - temp[j+i])
            y1 /= (start-1)
            y2 = temp[i+start] - temp[i+start-1]
            if abs(y2) > (y1*param):
                if y2 < 0:
                    temp[i+start] += abs(y2)
            y1 = 0
        ret.append(temp)
    return np.array(ret)


def reci(data):
    return 1/np.array(data)


def log(data):
    data_temp = []
    for _ in data:
        data_temp.append(math.log(_))
    return data_temp


def log_reci(data):
    data_temp = log(data)
    return 1/np.array(data_temp)


if __name__ == '__main__':
    main()