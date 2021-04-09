from 文件读取 import File
import 装饰器 as Wrapper
import numpy as np
from matplotlib import pyplot as plt
import sg平滑滤波 as Sg
import copy
目录 = 'C:/Users/liang-jiashun/Desktop/001'


@Wrapper.use_time(mode='s')
@Wrapper.列表循环(目录, enable_createFile=False)
def main(basic, path_train):
    plt.figure(figsize=(8, 4.5))
    # plt.axis([0, 18, 590, 700])
    ax = plt.gca()
    ax.invert_xaxis()
    plt.xticks(np.arange(1, 19))
    plt.xlabel('Number')
    plt.ylabel('Time')
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    # plt.title('Kalman',fontsize=18)
    print(path_train[1:])

    file = File(path_train, basic)
    temp = file.pop()
    while temp is not None:
        a, b, c = temp
        y = np.array(a) + np.array(b) - np.array(c)
        y[y > 700] = 700

        whole(y)

        temp = file.pop()
        # plt.legend([l1, l3], ['Raw data', 'Kalman'], loc='upper left', fontsize=18)
        # plt.show()
        # exit()
    # plt.legend([l1, l3], ['Moving average', 'Kalman'], loc = 'upper left', fontsize=18)
    plt.show()
    exit()


def whole(data):
    # l1, = plt.plot(range(len(data), 0, -1), data, color='g')

    data1 = ave(copy.deepcopy(data))
    l2, = plt.plot(range(len(data1), 0, -1), data1, color='r')

    # data2 = Sg.savgol(copy.deepcopy(data).tolist(), 3, 2)
    # l2, = plt.plot(range(len(data2), 0, -1), data2, color='b')
    # #
    data3 = kel(copy.deepcopy(data))[:len(data)]
    l3, = plt.plot(range(len(data3), 0, -1), data3, color='b')
    # plt.show()
    return


def whole1(data):
    # l1, = plt.plot(range(18, 18 - len(data[:14]), -1), data[:14])

    data2 = ave(copy.deepcopy(data))
    # l2, = plt.plot(range(len(data1), 0, -1), data1, color='b')

    # data2 = Sg.savgol(copy.deepcopy(data).tolist(), 3, 2)
    l1, = plt.plot(range(18, 18 - len(data2[:]), -1), data2[:], color='y')
    # #
    # data3 = kel(copy.deepcopy(data))[:len(data)-6]
    # l2, = plt.plot(range(18, 18-len(data3), -1), data3)
    # plt.show()
    return l1


def part3(data):
    plt.plot(range(len(data)), data)
    for i in range(len(data)-2):
        data1 = ave(copy.deepcopy(data[i:i+3]))
        plt.plot(range(i, i+3), data1)

        # data2 = Sg.savgol(copy.deepcopy(data[i:i + 3]).tolist(), 3, 2)
        # plt.plot(range(i, i+3), data2)

        # data3 = kel(copy.deepcopy(data[i:i + 3]))
        # plt.plot(range(i, i+3), data3)
    # plt.show()


def part(data):
    l1, = plt.plot(range(len(data), 0, -1), data)
    for i in range(len(data)-2):
        data1 = ave(copy.deepcopy(data[:i+3]))
        l2, = plt.plot(range(18, 18-len(data1), -1), data1, color='y')

        data2 = Sg.savgol(copy.deepcopy(data[:i + 3]).tolist(), 3, 2)
        l3, = plt.plot(range(18, 18-len(data2), -1), data2, color='g')

        data3 = kel(copy.deepcopy(data[:i + 3]))
        l4, = plt.plot(range(18, 18-len(data3), -1), data3, color='r')
    # plt.show()
    return l1, l2, l3, l4


def ave(data):
    window = [0.3, 0.3, 0.3]
    data[1] = (data[0] + data[1]) / 2
    for i in range(len(data[2:])):
        data[i + 2] = (data[i] * window[0] + data[i + 1] * window[1] + data[i + 2] * window[2])/sum(window)
    return data


def kel(data):
    n_iter = len(data)
    sz = n_iter
    Q = 9       # 处理误差 down
    R = 20      # 估计误差 up
    # 分配数组空间
    xhat = np.zeros(sz)
    P = np.zeros(sz)
    xhatminus = np.zeros(sz)
    Pminus = np.zeros(sz)
    K = np.zeros(sz)

    xhat[0] = data[0]
    P[0] = 10

    for k in range(1, n_iter):
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + Q

        K[k] = Pminus[k] / (Pminus[k] + R)
        xhat[k] = xhatminus[k] + K[k] * (data[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]

    return xhat


if __name__ == '__main__':
    main()
