from numpy import array
from numpy import log
from scipy.optimize import leastsq
from numpy import exp


class Poly:
    def __init__(self, cache):
        if cache is None:
            self.k = 0
            self.b = 0
        else:
            temp = eval(cache)
            self.k = temp[0]
            self.b = temp[1]
            print(temp)

    def fit(self, x_num, y_time):
        def err(p, xi, yi):
            return p[0] * xi + p[1] - yi

        x_num_temp = array(x_num)
        x_num_temp = log(x_num_temp)
        y_time_temp = array(y_time)

        p0 = array([100, 20])
        k, b = leastsq(err, p0, args=(x_num_temp, y_time_temp))[0]
        if self.k == 0 or self.b == 0:
            self.k = k
            self.b = b
        else:
            self.k = (self.k + k) / 2
            self.b = (self.b + b) / 2

        # import matplotlib.pyplot as plt
        # plt.scatter(exp(x_num_temp), y_time_temp, color="red", label="Sample Point", linewidth=3)
        # plt.plot(exp(x_num_temp), x_num_temp*self.k+self.b, color="orange", label="Fitting Line", linewidth=2)
        # plt.legend()
        # plt.show()