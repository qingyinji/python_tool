import numpy as np
import 获取数据 as getdata
import matplotlib.pyplot as plt


def main():
    path = "C:/Users/liang-jiashun/Desktop/0011.xlsx"
    this = getdata.get_data(path)
    plt.figure()
    plt.scatter(range(len(this.result2[0])), this.result2[0])
    res = savgol(this.result2[0], 3, 2)
    # plt.figure()
    plt.scatter(range(len(res)), res)
    res = np.convolve([0.2, 0.3, 0.5], this.result2[0])
    res[20] = res[19] = res[18]
    res[0] = res[1] = res[2]
    print(len(res))
    plt.scatter(range(len(res)), res)
    plt.show()
    print(len(res))




"""
* 创建系数矩阵X
* size - 2×size+1 = window_size
* rank - 拟合多项式阶次
* x - 创建的系数矩阵
"""
def create_x(size, rank):
    x = []
    for i in range(2 * size + 1):
        m = i - size
        row = [m**j for j in range(rank)]
        x.append(row)
    x = np.mat(x)
    return x

"""
 * Savitzky-Golay平滑滤波函数
 * data - list格式的1×n纬数据
 * window_size - 拟合的窗口大小
 * rank - 拟合多项式阶次
 * ndata - 修正后的值
"""
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


def fli(this):
    temp = []
    res = []
    for _ in this.data1:
        if _ == 0:
            res.extend(savgol(temp, 3, 2))
            temp.clear()
            continue
        temp.append(_)
    this.data1 = res
    res.clear()

    for _ in this.data2:
        if _ == 0:
            res.extend(savgol(temp, 3, 2))
            temp.clear()
            continue
        temp.append(_)
    this.data2 = res
    res.clear()

    for _ in this.data3:
        if _ == 0:
            res.extend(savgol(temp, 3, 2))
            temp.clear()
            continue
        temp.append(_)
    this.data3 = res
    res.clear()


if __name__ == '__main__':
    main()