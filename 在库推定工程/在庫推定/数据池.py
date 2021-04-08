from copy import deepcopy


class Pond:
    def __init__(self, pond_size=10):
        self.__size_max = pond_size
        # self.data_T = []
        self.dataA = []
        self.dataB = []
        self.dataC = []

    # def append(self, data):
    #     if len(self.data_T) < len(data):
    #         for i in range(len(data) - len(self.data_T)):
    #             self.data_T.append(list())
    #     for i, temp in enumerate(data):
    #         self.data_T[i].append(temp)
    #
    #         if len(self.data_T[i]) > self.__size_max:
    #             self.__adjust(i)
    def append(self, dataA, dataB, dataC):
        if len(self.dataA) < len(dataA):
            for i in range(len(dataA) - len(self.dataA)):
                self.dataA.append(list())
                self.dataB.append(list())
                self.dataC.append(list())
        for i in range(len(dataA)):
            self.dataA[i].append(dataA[i])
            self.dataB[i].append(dataB[i])
            self.dataC[i].append(dataC[i])

            if len(self.dataA[i]) > self.__size_max:
                self.__adjust(i)

    def get(self):
        return self.__adjust(None, copy_flag=True)
    #
    # def __adjust(self, row, copy_flag=False):
    #     if copy_flag:
    #         temp = deepcopy(self.data_T)
    #         for i, _ in enumerate(temp):
    #             if len(_) > 2:
    #                 temp[i].pop(max(_.index(max(_)), _.index(min(_))))
    #                 temp[i].pop(min(_.index(max(_)), _.index(min(_))))
    #         return temp
    #
    #     m = self.data_T[row].index(max(self.data_T[row]))
    #     n = self.data_T[row].index(min(self.data_T[row]))
    #     self.data_T[row].pop(max(m, n))
    #     self.data_T[row].pop(min(m, n))
    def __adjust(self, row, copy_flag=False):
        if copy_flag:
            temp1 = deepcopy(self.dataA)
            for i, _ in enumerate(temp1):
                if len(_) > 2:
                    temp1[i].pop(max(_.index(max(_)), _.index(min(_))))
                    temp1[i].pop(min(_.index(max(_)), _.index(min(_))))

            temp2 = deepcopy(self.dataB)
            for i, _ in enumerate(temp2):
                if len(_) > 2:
                    temp2[i].pop(max(_.index(max(_)), _.index(min(_))))
                    temp2[i].pop(min(_.index(max(_)), _.index(min(_))))

            temp3 = deepcopy(self.dataC)
            for i, _ in enumerate(temp3):
                if len(_) > 2:
                    temp3[i].pop(max(_.index(max(_)), _.index(min(_))))
                    temp3[i].pop(min(_.index(max(_)), _.index(min(_))))
            return temp1, temp2, temp3

        m = self.dataA[row].index(max(self.dataA[row]))
        n = self.dataA[row].index(min(self.dataA[row]))
        self.dataA[row].pop(max(m, n))
        self.dataA[row].pop(min(m, n))

        m = self.dataB[row].index(max(self.dataB[row]))
        n = self.dataB[row].index(min(self.dataB[row]))
        self.dataB[row].pop(max(m, n))
        self.dataB[row].pop(min(m, n))

        m = self.dataC[row].index(max(self.dataC[row]))
        n = self.dataC[row].index(min(self.dataC[row]))
        self.dataC[row].pop(max(m, n))
        self.dataC[row].pop(min(m, n))
