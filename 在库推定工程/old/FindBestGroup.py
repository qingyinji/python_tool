import LineMatch


def findgroup(this, num, num_max):
    param_group = []
    size = 25
    for line_flag in range(1,5):
        result = []
        for temp in this.data_train_fli:
             # 取多点作拟合优度计算，得到剩余数
            result_num = LineMatch.linematch(temp, this.list, num, num_max, line_flag)
            result.append(result_num)
        result.reverse()
        temp_group = 0
        for i in range(len(result)):
            temp_group += abs(result[i]-i-1)*int((size-i)/3)
        param_group.append(temp_group)
        result.clear()
    # print(param_group)
    bestgroup = []
    temp_best = 0
    for j in range(3):
        for i in range(int(len(param_group)/3)):
            temp_best += param_group[j*int(len(param_group)/3)+i]
        bestgroup.append(temp_best)
        temp_best = 0
    return bestgroup.index(min(bestgroup))+1
