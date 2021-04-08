import math


def linematch(data_wave, polynomial_list, num, num_max, flag):
    data_r2 = []
    result = []
    y3 = 0
    y2 = 0
    y1 = 0
    for i in range(num):
        data_r2.append(data_wave[len(data_wave) - num + i])
    # print("Date", num, ":", data_r2)
# -------------------------------------------------------------------
    if flag == 1:
        for j in range(0, num_max - num + 1):
            for i in range(0, num):
                y1 += abs(data_r2[i] - polynomial_list[j + i])
            result.append(y1)
            y1 = 0
        result_num = num_max - num + 1 - result.index(min(result))

# -------------------------------------------------------------------
    elif flag == 2:
        for j in range(0, num_max - num + 1):
            for i in range(0, num_max):
                y3 += polynomial_list[i]
            y3 /= num_max
            for i in range(0, num):
                y1 += pow(data_r2[i] - polynomial_list[j+i], 2)
                y2 += pow(polynomial_list[j + i] - y3, 2)
            result.append(1 - y1 / y2)
            y1 = 0
            y2 = 0
            y3 = 0
        result_num = num_max - num + 1 - result.index(max(result))

# -------------------------------------------------------------------
    elif flag == 3:
        for j in range(0, num_max - num + 1):
            for i in range(0, num):
                y1 += pow(data_r2[i] - polynomial_list[j + i], 2)
                y2 += pow(data_r2[i], 2)
            result.append(1 - math.sqrt(y1/y2))
            y1 = 0
            y2 = 0
        result_num = num_max - num + 1 - result.index(max(result))

    # print("Result:", result)
    # print("Number-->", result_num)
    return result_num
