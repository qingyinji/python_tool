import numpy as np
import sg平滑滤波 as Sg


def data_filter(data, mode='sg'):
    def mode_s(data_):
        if mode == 'sg':
            data_ = Sg.savgol(data_, 3, 2)

        elif mode == 'ave':
            window = [0.2, 0.3, 0.5]
            data_[1] = (data_[0] + data_[1])/2
            for i in range(len(data_[2:])):
                data_[i+2] = data_[i]*window[0] + data_[i+1]*window[1] + data_[i+2]*window[2]

        elif mode == 'kal':
            data_ = kalman(data_)

        return data_

    try:
        aaaa = np.array(data).shape[2]
        for i, abc in enumerate(data):
            for ii, abcd in enumerate(abc):
                data[i][ii] = mode_s(abcd)
    except IndexError:
        for i, abc in enumerate(data):
            data[i] = mode_s(abc)
    return data


def data_change(x):
    a = np.array(x[0])
    b = np.array(x[1])
    c = np.array(x[2])
    ret = a + b - c
    ret[ret > 1000] = 1000
    ret[ret < 400] = 400
    return ret.tolist()


def kalman(data):
    sz = len(data)
    Q = 10  # 处理误差 down
    R = 18  # 估计误差 up
    # 分配数组空间
    xhat = np.zeros(sz)
    P = np.zeros(sz)
    xhatminus = np.zeros(sz)
    Pminus = np.zeros(sz)
    K = np.zeros(sz)

    xhat[0] = data[0]
    P[0] = 1.0

    for k in range(1, sz):
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + Q

        K[k] = Pminus[k] / (Pminus[k] + R)
        xhat[k] = xhatminus[k] + K[k] * (data[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]

    return xhat
