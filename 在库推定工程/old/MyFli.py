from scipy import signal
import copy
import numpy


def my_fliter(data_input, flag):
    # filtfilt滤波器
    data_wave = []
    if flag == 1:
        db = 0.45
        bb, aa = signal.butter(1, db, 'lowpass')
        temp = signal.filtfilt(bb, aa, data_input)
        for _ in temp:
            data_wave.append(copy.deepcopy(_))
    # 加权滑动平均
    elif flag == 2:
        data_wave = []
        window = [0.2, 0.3, 0.6]
        data_wave.append(data_input[0])
        data_wave.append(0.2*data_input[0] + 0.8*data_input[1])
        data_wave.append(window[0]*data_input[0] + window[1]*data_input[1] + window[2]*data_input[2])
        for i in range(len(data_input)-3):
            data_wave.append(window[0]*data_input[i+1] + window[1]*data_input[i+2] + window[2]*data_input[i+3])

    # 滑动平均 (无权重)
    elif flag == 3:
        data_wave = []
        window = [0.333, 0.333, 0.333]
        data_wave.append(data_input[0])
        data_wave.append(0.2 * data_input[0] + 0.8 * data_input[1])
        data_wave.append(window[0] * data_input[0] + window[1] * data_input[1] + window[2] * data_input[2])
        for i in range(len(data_input) - 3):
            data_wave.append(
                window[0] * data_input[i + 1] + window[1] * data_input[i + 2] + window[2] * data_input[i + 3])

    # 卡尔曼滤波
    elif flag == 4:
        n_iter = len(data_input)
        sz = (n_iter)
        Q = 1e-2
        # 分配数组空间
        xhat = numpy.zeros(sz)
        P = numpy.zeros(sz)
        xhatminus = numpy.zeros(sz)
        Pminus = numpy.zeros(sz)
        K = numpy.zeros(sz)

        R = 0.1**2

        xhat[0] = data_input[0]
        P[0] = 1.0

        for k in range(1, n_iter):
            xhatminus[k] = xhat[k-1]
            Pminus[k] = P[k-1] + Q

            K[k] = Pminus[k] / (Pminus[k] + R)
            xhat[k] = xhatminus[k] + K[k] * (data_input[k] - xhatminus[k])
            P[k] = (1 - K[k]) * Pminus[k]

        for _ in xhat:
            data_wave.append(copy.deepcopy(_))

    elif flag == 5:
        import sg平滑滤波 as sg
        res = sg.savgol(data_input, 3, 2)
        data_wave = list(res)

    return data_wave
