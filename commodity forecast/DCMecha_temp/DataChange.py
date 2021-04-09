import numpy as np


def data_filter(data, mode='sg'):
    def mode_s(data_):
        data_ = kalman(data_)
        return data_

    try:
        aaaa = np.array(data).shape[2]
        for i, abc in enumerate(data):
            for ii, abcd in enumerate(abc):
                data[i][ii] = mode_s(abcd)
    except IndexError:
        data = np.array(data).T
        data = data.tolist()
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
    n_iter = len(data)
    sz = n_iter
    Q = 10  # 处理误差 down
    R = 18  # 估计误差 up
    # 分配数组空间
    xhat = np.zeros(sz)
    P = np.zeros(sz)
    xhatminus = np.zeros(sz)
    Pminus = np.zeros(sz)
    K = np.zeros(sz)

    xhat[0] = min(data[0:3])
    P[0] = 1.0

    for k in range(1, n_iter):
        xhatminus[k] = xhat[k - 1]
        Pminus[k] = P[k - 1] + Q

        K[k] = Pminus[k] / (Pminus[k] + R)
        xhat[k] = xhatminus[k] + K[k] * (data[k] - xhatminus[k])
        P[k] = (1 - K[k]) * Pminus[k]

    return xhat


def create_x(size, rank):
    x = []
    for i in range(2 * size + 1):
        m = i - size
        row = [m**j for j in range(rank)]
        x.append(row)
    x = np.mat(x)
    return x


def savgol(data, window_size, rank):
    m = int((window_size - 1) / 2)
    odata = data[:]
    # 处理边缘数据，首尾增加m个首尾项
    for i in range(m):
        odata.insert(0,odata[0])
        odata.insert(len(odata),odata[len(odata)-1])
    # 创建X矩阵
    x = create_x(m, rank)
    # 计算加权系数矩阵B
    b = (x * (x.T * x).I) * x.T
    a0 = b[m]
    a0 = a0.T
    # 计算平滑修正后的值
    ndata = []
    for i in range(len(data)):
        y = [odata[i + j] for j in range(window_size)]
        y1 = np.mat(y) * a0
        y1 = float(y1)
        ndata.append(y1)
    return ndata
