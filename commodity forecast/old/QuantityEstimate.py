import Polyamorphic
import LineMatch
import MyFli
import DelErrorDate
import WriteExcel
import FindBestGroup
import copy


def quantityestimate(indata_train, indata_test, path_data, *args):
    # -----------------------------------------------------------------------------------------------------
    # 数据来源     1:测试数据       2：虚拟数据1     3:虚拟数据2
    data_flag = 1

    # 拟合方式  1：累加    2：多项式   3：对数    4: 累加（矩阵排序，去除头尾项）
    poli_flag = 4

    # 线段匹配算法 0:自动选择    1：线段距离   2：R^2拟合优度    3：Rnew拟合优度    4：单个匹配
    line_flag = 3

    # 曲线匹配规则  num：线段长度   num_max：最大估计值
    num = 3
    num_max = 20

    # 滤波  1:flitflit滤波 系数 0.4  2:加权滑动滤波 滑动窗口：0.2 0.3 0.5    3：滑动平均    4:卡尔曼滤波
    fli_flag = 2

    # 更新拟合数据要求的最低连续数据
    update_flag = 1
    # -----------------------------------------------------------------------------------------------------

    class Object:
        list = []  # 参考表
        start = 0

        path_train = ''
        data_train = []
        data_train_fli = []

        path_test = ''
        data_test = []

        dateTable = []
        polynomial = [0, 0, 0, 0]
        a = 0
        b = 0
        time = 0
    # -----------------------------------------------------------------------------------------------------

    this = Object()
    this.data_train = indata_train[0]
    this.data_test = indata_test

    for temp in this.data_train:                      # 舍弃第一个数据
        temp.pop(0)
    for temp in this.data_test:
        temp.pop(0)

    for temp in this.data_train:
        DelErrorDate.errordate(temp)                                    # 消除数据中异常大幅降低的值

    for temp in this.data_train:
        this.data_train_fli.append(copy.deepcopy(MyFli.my_fliter(temp, fli_flag)))         # 过滤

    for temp in this.data_train_fli:
        Polyamorphic.polyamorphic(temp, this, poli_flag)      # 拟合

    Polyamorphic.polyamorphic_calculation(this, num_max, poli_flag)  # 获得参数表

    if poli_flag == 1 or poli_flag == 4:
        num_max = len(this.list)

    if line_flag == 0:                                               # 当line_flag == 0时，自动选择结果最好的估算方法
        line_flag = FindBestGroup.findgroup(this, num, num_max)
        print('Select the best LineMatch:',line_flag)

    result = []
    WriteExcel.initexcel(path_data)

    res = []
    for temp in this.data_test:
        if fli_flag == 2 or fli_flag == 3 or fli_flag == 4 or fli_flag == 5:
            times = 3
        elif fli_flag == 1:
            times = 7
        if times > len(temp):
            continue
        for _ in range(len(temp)-times+1):
            data_temp = temp[:times+_]

            DelErrorDate.errordate(data_temp)     # 消除数据中异常大幅降低的值
            data_temp = MyFli.my_fliter(data_temp, fli_flag)        # 过滤

            # 取多点作拟合优度计算，得到剩余数
            result_num = LineMatch.linematch(data_temp, this.list, num, num_max, line_flag)-0
            result.append(result_num)
        print('数量估计：', result)
        res.append(copy.deepcopy(result))
        WriteExcel.writeexcel(result, path_data)      # 将结果写入Excel中

        if update_flag > 0:
            Polyamorphic.polyamorphic_update(result, data_temp, this, update_flag, poli_flag)        # 更新拟合曲线
            Polyamorphic.polyamorphic_calculation(this, num_max, poli_flag)  # 计算获得参数表
        result.clear()

    return res
