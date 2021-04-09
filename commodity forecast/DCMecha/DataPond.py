from numpy import array
from numpy import log


class Pond:
    def __init__(self):
        temp = array(range(1, 50))
        temp = log(temp)
        self.table = temp.tolist()
