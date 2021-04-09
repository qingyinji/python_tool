import math
import numpy as np
from copy import deepcopy
import 在庫推定.数据变换 as Change


class Poly:
    def __init__(self, pond, mode='poly'):
        self.pond = pond
        self.__mode = mode
        self.table = []

    def fit(self):
        self.table.clear()
        if self.__mode == 'ave':
            temp1, temp2, temp3 = self.pond.get()
            for i in range(len(temp1)):
                temp = Change.data_change(temp1[i], temp2[i], temp3[i])
                self.table.append(sum(temp)/len(temp))
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
            result = []
            table = self.table
            for i in range(len(table) - 2):
                y = np.array(table[i:i+3])
                dist = np.linalg.norm(x - y)
                result.append(dist)
            res = result.index(min(result)) + 1

        else:
            print('Poly.predict(): no \'{}\' mode! Check it!'.format(mode))
            exit()

        return res
