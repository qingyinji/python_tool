import Polyamorphic
import ReadFile
import LineMatch
import MyFli
import DelErrorDate
import MyPlot
import WriteExcel
import FindBestGroup
# -----------------------------------------------------------------------------------------------------
# 曲线匹配规则  num：线段长度   num_max：最大估计值
num = 3
num_max = 15

# 线段匹配算法 0:自动选择1-3    1：线段距离   2：R^2拟合优度    3：Rnew拟合优度
line_flag = 0

# 滤波  1:flitflit滤波 系数 0.4  2:滑动滤波 滑动窗口：0.2 0.3 0.5
fli_flag = 2

# 更新拟合数据要求的最低连续数据
update_flag = 5

# path：训练数据     path1：测试数据
path = "E:/input.log"
path1 = "E:/input2.log"
#
polynomial_list = []
# -----------------------------------------------------------------------------------------------------
polynomial = [0, 0, 0, 0]

data_train = []
data_test = []
ReadFile.readfile(path, data_train) # 读取训练数据
ReadFile.readfile(path1, data_test) # 读取测试数据

# MyPlot.myplot(0)

# 拟合多组曲线，系数做递推权重相加
data_fit = []
for data_temp in data_train:
    if data_temp != 0:
        data_fit.append(data_temp)
    else:
        DelErrorDate.errordate(data_fit)   # 消除数据中异常大幅降低的值
        polynomial = Polyamorphic.polyamorphic(MyFli.my_fliter(data_fit, fli_flag), polynomial) # 取得拟合参数

        # MyPlot.myplot(2, MyFli.my_fliter(data_fit, fli_flag))

        data_fit.clear()
polynomial_list = Polyamorphic.polyamorphic_calculation(polynomial, num_max) # 计算获得参数表

if line_flag == 0:
    line_flag = FindBestGroup.findgroup(data_train, polynomial_list, num, num_max)
    print('Select the best LineMatch:',line_flag)

# MyPlot.myplot(1, polynomial)  # 画拟合曲线

result = []
data_test_temp = []
WriteExcel.initexcel()
for data_temp in data_test:
    if data_temp != 0:
        data_test_temp.append(data_temp)
    else:
        DelErrorDate.errordate(data_test_temp)     # 消除数据中异常大幅降低的值
        if fli_flag == 2:
            times = 2
        elif fli_flag == 1:
            times = 6
        for i in range(times, len(data_test_temp)):
            temp = []
            for ii in range(i+1):
                temp.append(data_test_temp[ii])

            # 滤波  Flag: 1 flitflit滤波 系数 0.4
            #             2 滑动平均 3 权重 0.2 0.3 0.5
            data_wave = MyFli.my_fliter(temp, fli_flag)

            # 取多点作拟合优度计算，得到剩余数
            result_num = LineMatch.linematch(data_wave, polynomial_list, num, num_max, line_flag)
            print("Number-->", result_num)
            result.append(result_num)
        WriteExcel.writeexcel(result)      # 将结果写入Excel中

        Polyamorphic.polyamorphic_update(result, data_test_temp, polynomial, update_flag)        # 更新拟合曲线
        polynomial_list = Polyamorphic.polyamorphic_calculation(polynomial, num_max)  # 计算获得参数表

        result.clear()
        data_test_temp.clear()

# myplot.myplot(10)
