import numpy
import pylab

# 这里是假设A=1，H=1的情况
# 参数初始化  
n_iter = 50
sz = (n_iter,)  # size of array
x = -0.5  # truth value (typo in example at top of p. 13 calls this z)真实值
z = numpy.random.normal(x, 0.1, size=sz)  # observations (normal about x, sigma=0.1)观测值

Q = 1e-5  # process variance

# 分配数组空间  
xhat = numpy.zeros(sz)  # a posteri estimate of x 滤波估计值
P = numpy.zeros(sz)  # a posteri error estimate滤波估计协方差矩阵
xhatminus = numpy.zeros(sz)  # a priori estimate of x 估计值
Pminus = numpy.zeros(sz)  # a priori error estimate估计协方差矩阵
K = numpy.zeros(sz)  # gain or blending factor卡尔曼增益

R = 0.1 ** 2  # estimate of measurement variance, change to see effect

# intial guesses  
xhat[0] = 0.0
P[0] = 1.0

for k in range(1, n_iter):
    # 预测  
    xhatminus[k] = xhat[k - 1]  # X(k|k-1) = AX(k-1|k-1) + BU(k) + W(k),A=1,BU(k) = 0
    Pminus[k] = P[k - 1] + Q  # P(k|k-1) = AP(k-1|k-1)A' + Q(k) ,A=1

    # 更新  
    K[k] = Pminus[k] / (Pminus[k] + R)  # Kg(k)=P(k|k-1)H'/[HP(k|k-1)H' + R],H=1
    xhat[k] = xhatminus[k] + K[k] * (z[k] - xhatminus[k])  # X(k|k) = X(k|k-1) + Kg(k)[Z(k) - HX(k|k-1)], H=1
    P[k] = (1 - K[k]) * Pminus[k]  # P(k|k) = (1 - Kg(k)H)P(k|k-1), H=1

pylab.figure()
pylab.plot(z, 'k+', label='noisy measurements')  # 观测值
pylab.plot(xhat, 'b-', label='a posteri estimate')  # 滤波估计值
pylab.axhline(x, color='g', label='truth value')  # 真实值
pylab.legend()
pylab.xlabel('Iteration')
pylab.ylabel('Voltage')
pylab.show()
