from scipy.optimize import leastsq
import math
import numpy as np
import copy

time = 3
# aa:训练拟合权重
aa = 0.8
# bb:更新拟合权重
bb = 0.9


##需要拟合的函数func :指定函数的形状 k= 0.42116973935 b= -8.28830260655
def func(p, x):
    k, b = p
    return k * x + b

##偏差函数：x,y都是列表:这里的x,y更上面的Xi,Yi中是一一对应的
def error(p, x, y):
    return func(p, x) - y

def polyamorphic(data, this, poli_flag, *args):
    if poli_flag == 1:   # 累加
        return

    elif poli_flag == 2:
        flag = 0
        z1 = np.polyfit(list(range(len(data), 0, -1)), data, time)
        p1 = np.poly1d(z1)

        if (this.polynomial[0] + this.polynomial[1] + this.polynomial[2] + this.polynomial[3]) == 0:
            flag = 1
        else:
            flag = 0
        if flag != 1:
            for i in range(time+1):
                if args:
                    this.polynomial[i] = (1 - bb) * p1[i] + bb * this.polynomial[i]
                else:
                    this.polynomial[i] = (1-aa) * p1[i] + aa * this.polynomial[i]
        else:
            for i in range(time+1):
                this.polynomial[i] = p1[i] + this.polynomial[i]

    elif poli_flag == 3:
        x = []
        for i in range(len(data), 0, -1):
            x.append(math.log(i))
        yi = np.array(data)
        xi = np.array(x)

        # k,b的初始值，可以任意设定,经过几次试验，发现p0的值会影响cost的值：Para[1]
        p0 = [-10, 700]
        # 把error函数中除了p0以外的参数打包到args中(使用要求)
        Para = leastsq(error, p0, args=(xi, yi))
        # 读取结果
        if this.a == 0 or this.b == 0:
            this.a, this.b = Para[0]
        else:
            a, b = Para[0]
            this.a = this.a*0.5 + a*0.5
            this.b = this.b*0.5 + b*0.5

    elif poli_flag == 4:
        if len(this.dateTable) < 10:
            this.dateTable.append(copy.deepcopy(data))
            max_temp = 0
            for _ in this.dateTable:
                if len(_) > max_temp:
                    max_temp = len(_)
            for _ in this.dateTable:
                if len(_) < max_temp:
                    while range(max_temp - len(_)):
                        _.append(0)

            temp = list(map(list, zip(*this.dateTable)))
            for _ in temp:
                _.sort()
            this.dateTable = list(map(list, zip(*temp)))
        elif len(this.dateTable) == 10:
            this.dateTable.pop(0)
            this.dateTable.pop(-1)

    return


def polyamorphic_calculation(this, num_max, flag, *args):
    this.list.clear()
    if flag == 1:
        if args:
            data = this.data_test_fli
        else:
            data = this.data_train_fli
        this.list.reverse()
        for _ in data:
            _.reverse()
            this.time += 1
            for i in range(len(_)):
                temp = _[i]
                if i >= len(this.list):
                    this.list.append(temp)
                else:
                    this.list[i] = (this.list[i]*(this.time-1) + temp)/(this.time)
            _.reverse()
        this.list.reverse()

    elif flag == 2:
        for _ in range(num_max, 0, -1):
            this.list.append(pow(_, 3) * this.polynomial[3] + pow(_, 2) * this.polynomial[2] + _ * this.polynomial[1] + this.polynomial[0])
        return

    elif flag == 3:
        for _ in range(num_max, 0, -1):
            this.list.append(this.a*math.log(_)+this.b)
        return

    elif flag == 4:
        for _ in list(map(list, zip(*this.dateTable))):
            jj = 0
            for ii in _:
                if ii == 0:
                    jj += 1
                else:
                    break
            mid_temp = _[jj:]
            if len(mid_temp) > 1:
                avg = np.average(mid_temp)
            else:
                avg = mid_temp[jj]
            this.list.append(avg)

        return


def polyamorphic_update(result, data, this, flag, poli_flag):
    if len(result) < flag:
        return
    result.reverse()
    for i in range(result[0], result[0]+flag):
        if i != result[i-result[0]]:
            result.reverse()
            return
    polyamorphic(data, this, poli_flag)
    print('Polyamorphic has Updated！！')
    result.reverse()
    return
