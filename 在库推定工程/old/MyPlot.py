import matplotlib.pyplot as pl
import numpy as np


def myplot(flag, *args):
    size1 = 10
    size2 = 4
    if flag == 1:
        # pl.figure(figsize=(size1, size2))
        if args:
            polynomial = args[0]
            x = np.arange(11, 1, -0.1)
            y = pow(x, 3) * polynomial[3] + pow(x, 2) * polynomial[2] + x * polynomial[1] + polynomial[0]
            pl.plot(x, y)
            pl.gca().invert_xaxis()

    elif flag == 0:
        pl.figure(figsize=(size1, size2))

    elif flag == 10:
        pl.show()

    elif flag == 2:
        # pl.figure(figsize=(size1, size2))
        if args:
            data = args[0]
            x = np.arange(len(data), 0, -1)
            pl.plot(x, data)
            pl.gca().invert_xaxis()
    return
