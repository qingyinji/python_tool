import math
import numpy as np


class Poly:
    table = []
    tableABC = []
    __mode = ''

    def __init__(self, mode='poly'):
        self.__mode = mode
        self.table.clear()
        self.tableABC.clear()

    def fit(self, x, y):
        if self.__mode == 'ave':
            self.table = ave(x, y)
            # import sg平滑滤波 as sg
            # self.table = sg.savgol(self.table, 3, 2)

        else:
            print('Poly.fit(): no \'{}\' mode! Check it!'.format(self.__mode))
            exit()

    def predict(self, x, mode='one', 最大估计值=20, 线段长度=3):
        res = 0
        if mode == 'one':
            for index, _ in enumerate(self.table):
                if x[-1] <= _:
                    res = len(self.table)-index
                    break
            else:
                res = 1

        elif mode == 'rnew':
            temp = x[-3:]
            result = []
            y1 = y2 = 0
            for j in range(len(self.table) - 线段长度 + 1):
                for i in range(线段长度):
                    y1 += pow(temp[i] - self.table[j + i], 2)
                    y2 += pow(temp[i], 2)
                result.append(1 - math.sqrt(y1 / y2))
                y1 = 0
                y2 = 0
            res = len(result) - result.index(max(result))

        elif mode == 'o':
            x = np.array(x)
            result = []
            table = self.table
            for i in range(len(table) - 2):
                y = np.array(table[i:i+3])
                dist = np.linalg.norm(x - y)
                result.append(dist)
            result.reverse()
            res = result.index(min(result)) + 1

        elif mode == 'o_O':
            a = np.array(x[0][-3:])
            b = np.array(x[1][-3:])
            c = np.array(x[2][-3:])
            x = np.array([a, b, c])
            result = []
            table = self.tableABC
            for i in range(len(table[0]) - 2):
                y = np.array([table[0][i:i+3], table[1][i:i+3], table[2][i:i+3]])
                dist = np.linalg.norm(x - y)
                result.append(dist)
            result.reverse()
            res = result.index(min(result)) + 1

        else:
            print('Poly.predict(): no \'{}\' mode! Check it!'.format(mode))
            exit()

        return res


def ave(x, y):
    from itertools import chain
    group_len = len(y[0])
    xx = list(chain.from_iterable(x))
    yy = list(chain.from_iterable(y))
    temp = [0 for i in range(group_len)]
    for i, _ in enumerate(yy):
        if temp[_ - 1] == 0:
            temp[_ - 1] = xx[i]
            continue
        temp[_ - 1] = (temp[_ - 1] + xx[i]) / 2
    temp.reverse()
    return temp.copy()


def ave_ABC(x, y):
    from itertools import chain
    group_len = len(y[0])
    a = x[0]
    b = x[1]
    c = x[2]
    aa = list(chain.from_iterable(a))
    bb = list(chain.from_iterable(b))
    cc = list(chain.from_iterable(c))
    yy = list(chain.from_iterable(y))
    temp1 = [0 for i in range(group_len)]
    for i, _ in enumerate(yy):
        if temp1[_ - 1] == 0:
            temp1[_ - 1] = aa[i]
            continue
        temp1[_ - 1] = (temp1[_ - 1] + aa[i]) / 2
    temp1.reverse()

    temp2 = [0 for i in range(group_len)]
    for i, _ in enumerate(yy):
        if temp2[_ - 1] == 0:
            temp2[_ - 1] = bb[i]
            continue
        temp2[_ - 1] = (temp2[_ - 1] + bb[i]) / 2
    temp2.reverse()

    temp3 = [0 for i in range(group_len)]
    for i, _ in enumerate(yy):
        if temp3[_ - 1] == 0:
            temp3[_ - 1] = cc[i]
            continue
        temp3[_ - 1] = (temp3[_ - 1] + cc[i]) / 2
    temp3.reverse()
    return [temp1.copy(), temp2.copy(), temp3.copy()]
