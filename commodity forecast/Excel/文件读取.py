import 获取数据 as Get
import WriteExcel
import os
import shutil
import copy


class File:
    a = []
    b = []
    c = []

    def __init__(self, path, basic, createFile=True):
        # ---------------------- 读取数据输入文件
        self.a.clear()
        self.b.clear()
        self.c.clear()
        this = Get.get_data(basic + path, head_del=False)
        try:
            for i in range(int(len(this.data1) / this.data1.index(0))):
                self.a.append(copy.deepcopy(this.data1[this.data1.index(0) * i + i:this.data1.index(0) * (i + 1) + i]))
                self.b.append(copy.deepcopy(this.data2[this.data2.index(0) * i + i:this.data2.index(0) * (i + 1) + i]))
                self.c.append(copy.deepcopy(this.data3[this.data3.index(0) * i + i:this.data3.index(0) * (i + 1) + i]))
        except IndexError:
            self.a.append(copy.deepcopy(this.data1))
            self.b.append(copy.deepcopy(this.data2))
            self.c.append(copy.deepcopy(this.data3))

        # --------------------------------- 生成输出文件
        if createFile:
            if not os.path.exists(basic + "/test"):  # 创建test目录
                os.makedirs(basic + "/test")

            if os.path.exists(basic + "/test/test_" + path[1:]):
                os.remove(basic + "/test/test_" + path[1:])
            shutil.copy("C:/Users/liang-jiashun/Desktop/Excel模板/test.xlsx", basic + "/test")
            os.rename(basic + "/test/test.xlsx", basic + "/test/test_" + path[1:])
            WriteExcel.initexcel(basic + "/test/test_" + path[1:])

    def pop(self):
        try:
            return self.a.pop(0), self.b.pop(0), self.c.pop(0)
        except IndexError:
            return None


def main():
    pass


if __name__ == '__main__':
    main()