import math


def linematch(data_wave, polynomial_list, num, num_max, flag):
    if len(data_wave) < 3:
        return
    temp = data_wave[len(data_wave)-3:len(data_wave)]

    result = []
    result_num = 0
    y2 = 0
    y1 = 0
# -------------------------------------------------------------------
    if flag == 1:
        end_flag = 0
        for j in range(0, num_max - num + 1):
            for i in range(num):
                if (j+num) > len(polynomial_list):
                    end_flag = 1
                    break;
                y1 += abs(temp[i] - polynomial_list[j + i])
            if end_flag ==1:
                break
            result.append(y1)
            y1 = 0
        result_num = len(result) - result.index(min(result))

# -------------------------------------------------------------------
    elif flag == 2:
        for i in range(len(polynomial_list)-2):
            y3 = (polynomial_list[i]+polynomial_list[i+1]+polynomial_list[i+2])/3
            for j in range(num):
                y1 += pow(temp[j] - y3, 2)
                y2 += pow(polynomial_list[j + i] - y3, 2)
            result.append(y1 / y2)
            y1 = 0
            y2 = 0
        result_num = len(result) - result.index(min(result))

# -------------------------------------------------------------------
    elif flag == 3:
        for j in range(0, num_max - num + 1):
            for i in range(0, num):
                y1 += pow(temp[i] - polynomial_list[j + i], 2)
                y2 += pow(temp[i], 2)
            result.append(1 - math.sqrt(y1/y2))
            y1 = 0
            y2 = 0
        result_num = len(result) - result.index(max(result))

# -------------------------------------------------------------------
    elif flag == 4:
        aa = temp[len(temp)-1]
        index = -1
        for _ in polynomial_list:
            index += 1
            if aa > _:
                continue
            if (index > 0) and (index < (len(polynomial_list) - 1)):
                if abs(polynomial_list[index]-aa) > abs(polynomial_list[index-1]-aa):
                    result_num = len(polynomial_list) - index + 1
                else:
                    result_num = len(polynomial_list) - index
            elif index == 0:
                result_num = len(polynomial_list)
            elif index == (len(polynomial_list)-1):
                result_num = 1
            break

        if index == len(polynomial_list)-1:
            result_num = 1

    return result_num
