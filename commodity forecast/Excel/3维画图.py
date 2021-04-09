import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import 获取数据 as getdata
import os


def main():
    path_bath = "0001"
    path_src = "C:/Users/liang-jiashun/Desktop" + "/" + path_bath
    files = os.listdir(path_src)
    for i, file in enumerate(files):
        if not os.path.isdir(path_src + "/" + file):
            print(file)
            this = getdata.get_data(path_src + "/" + file)

            while 0 in this.data1:
                this.data1.remove(0)
                this.data2.remove(0)
                this.data3.remove(0)
                this.y.remove(0)

            # ax3d(change.log(this.data1), change.log(this.data2), change.log(this.data3), file)
            ax3d(this.data1, this.data2, this.data3, file)
            # break
    plt.show()


def ax3d(x, y, z, *args):
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 用来正常显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z)
    if args:
        ax.set_title(args[0])
    ax.set_xlabel('A', fontdict={'size': 15, 'color': 'red'})
    ax.set_ylabel('B', fontdict={'size': 15, 'color': 'red'})
    ax.set_zlabel('C', fontdict={'size': 15, 'color': 'red'})


if __name__ == '__main__':
    main()
