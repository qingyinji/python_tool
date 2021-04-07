import LineMatch
import MyFli
import DelErrorDate


def findgroup(data_test, polynomial_list, num, num_max):
    param_group = []
    size = 25
    for line_flag in range(1,4):
        fli_flag = 2
        result = []
        data_test_temp = []
        for data_temp in data_test:
            if data_temp != 0:
                data_test_temp.append(data_temp)
            else:
                DelErrorDate.errordate(data_test_temp)  # 消除数据中异常大幅降低的值
                if fli_flag == 2:
                    times = 2
                elif fli_flag == 1:
                    times = 6
                for i in range(times, len(data_test_temp)):
                    temp = []
                    for ii in range(i + 1):
                        temp.append(data_test_temp[ii])

                    # 滤波  Flag: 1 flitflit滤波 系数 0.4
                    #             2 滑动平均 3 权重 0.2 0.3 0.5
                    data_wave = MyFli.my_fliter(temp, fli_flag)

                    # 取多点作拟合优度计算，得到剩余数
                    result_num = LineMatch.linematch(data_wave, polynomial_list, num, num_max, line_flag)
                    result.append(result_num)
                result.reverse()
                temp_group = 0
                for i in range(len(result)):
                    temp_group += abs(result[i]-i-1)*int((size-i)/3)
                param_group.append(temp_group)
                result.clear()
                data_test_temp.clear()
    # print(param_group)
    bestgroup = []
    temp_best = 0
    for j in range(3):
        for i in range(int(len(param_group)/3)):
            temp_best += param_group[j*int(len(param_group)/3)+i]
        bestgroup.append(temp_best)
        temp_best = 0
    return bestgroup.index(min(bestgroup))+1
