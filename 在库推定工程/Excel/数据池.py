import numpy as np
import copy


class Pond:
    def __init__(self, pond_size=10):
        self.__group_max = pond_size
        self.pondA = []
        self.pondB = []
        self.pondC = []
        self.group_size = 0

    def append(self, data):
        self.pondA.append(data[0])
        self.pondB.append(data[1])
        self.pondC.append(data[2])
        self.group_size = len(self.pondA[0])
        if len(self.pondA) > self.__group_max:
            self.__adjust()

    def get(self):
        if len(self.pondA) > 2:
            data_x = list(self.__adjust(copy_=True))
        else:
            data_x = [self.pondA, self.pondB, self.pondC]
        data_y = []
        for i in range(len(data_x[0])):
            temp = []
            for ii in range(len(self.pondA[0])):
                temp.append(ii + 1)
            temp.reverse()
            data_y.append(copy.deepcopy(temp))
        return data_x, data_y

    def __adjust(self, copy_=False):
        def tt(data):
            temp_ = np.array(data).T
            temp_ = temp_.tolist()
            return temp_
        temp = np.array(self.pondA) + np.array(self.pondB) - np.array(self.pondC)
        temp = temp.T
        temp = temp.tolist()
        A = tt(self.pondA)
        B = tt(self.pondB)
        C = tt(self.pondC)
        for index, _ in enumerate(temp):
            m = _.index(max(_))
            n = _.index(min(_))
            A[index].pop(max(m, n))
            A[index].pop(min(m, n))
            B[index].pop(max(m, n))
            B[index].pop(min(m, n))
            C[index].pop(max(m, n))
            C[index].pop(min(m, n))
        if copy_:
            return tt(A), tt(B), tt(C)
        self.pondA = tt(A)
        self.pondB = tt(B)
        self.pondC = tt(C)
