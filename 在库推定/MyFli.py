from scipy import signal


def my_fliter(data_input, flag):
    # filtfilt滤波器
    if flag == 1:
        db = 0.45
        bb, aa = signal.butter(1, db, 'lowpass')
        data_wave = signal.filtfilt(bb, aa, data_input)
    # 滑动平均
    if flag == 2:
        data_wave = []
        window = [0.2, 0.3, 0.5]
        data_wave.append(data_input[0])
        data_wave.append(0.2*data_input[0] + 0.8*data_input[1])
        data_wave.append(window[0]*data_input[0] + window[1]*data_input[1] + window[2]*data_input[2])
        for i in range(len(data_input)-3):
            data_wave.append(window[0]*data_input[i+1] + window[1]*data_input[i+2] + window[2]*data_input[i+3])

    return data_wave
