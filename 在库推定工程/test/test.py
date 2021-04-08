import numpy as np
import pylab as pl

import polyamorphic
import readfile
import linematch
import myfil
import errordate

num = 3
num_line = 10
path = "E:/input.log"
path1 = "E:/test.log"
polynomial = [0, 0, 0, 0]
temp = "y"
dataArray = []
data_input = []

readfile.readfile(path, dataArray)

readfile.readfile(path1, data_input)

errordate.errordate(data_input)

if temp == "y":
    index = 0
    data_fit = []
    for data_temp in dataArray:
        if data_temp != 0:
            data_fit.append(data_temp)
        else:
            index += 1
            polynomial = polyamorphic.polyamorphic(data_fit, polynomial)
            data_fit.clear()
    print("Data Number:", len(dataArray), "    Group Number:", index)
    print(dataArray)
    print("y = (", polynomial[3], ")*x^3+", "(", polynomial[2], ")*x^2+", "(", polynomial[1], ")*x+", "(", polynomial[0], "）")

    x = np.arange(11, 1, -0.1)
    y = pow(x, 3) * polynomial[3] + pow(x, 2) * polynomial[2] + x * polynomial[1] + polynomial[0]
    pl.figure(figsize=(10, 4))
    # pl.subplot(211)
    # data_plot = []
    # for data_temp in dataArray:
    #     if data_temp != 0:
    #         data_plot.append(data_temp)
    #     else:
    #         pl.plot(np.arange(len(data_plot), 0, -1), data_plot)
    #         data_plot.clear()
    # pl.plot(x, y, label='polynomial')
    # pl.gca().invert_xaxis()

    # pl.subplot(212)
    pl.plot(x, y)

    data_wave = myfil.my_filter(data_input, 1)

    print("Wave:", data_wave)
    # pl.plot(np.arange(len(data_input2), len(data_input2) - len(data_input), -1), data_wave)

    result_num, data_r2 = linematch.linematch(data_wave, polynomial, num, num_line, 2)

    pl.plot(range(result_num + num - 1, result_num - 1, -1), data_r2)
    pl.gca().invert_xaxis()
    pl.show()

