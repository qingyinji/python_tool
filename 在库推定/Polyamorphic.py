import numpy as np
time = 3
# aa:训练拟合权重
aa = 0.8
# bb:更新拟合权重
bb = 0.9


def polyamorphic(data, param, *args):
    flag = 0

    z1 = np.polyfit(list(range(len(data), 0, -1)), data, time)
    p1 = np.poly1d(z1)

    if (param[0] + param[1] + param[2] + param[3]) == 0:
        flag = 1
    if flag != 1:
        for i in range(time+1):
            if args:
                param[i] = (1 - bb) * p1[i] + bb * param[i]
            else:
                param[i] = (1-aa) * p1[i] + aa * param[i]
    else:
        for i in range(time+1):
            param[i] = p1[i] + param[i]
    return param


def polyamorphic_calculation(polynomial, num_max):
    polyamorphic_list = []
    for _ in range(num_max, 0, -1):
        polyamorphic_list.append(pow(_, 3) * polynomial[3] + pow(_, 2) * polynomial[2] + _ * polynomial[1] + polynomial[0])
    return polyamorphic_list

def polyamorphic_update(result, data, param, flag):
    if len(result) < flag:
        return
    result.reverse()
    for i in range(result[0], result[0]+flag):
        if i != result[i-result[0]]:
            result.reverse()
            return
    polyamorphic(data, param, 1)
    print('Polyamorphic has Updated！！')
    result.reverse()
    result
