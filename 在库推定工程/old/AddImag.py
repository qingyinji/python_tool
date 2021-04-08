import os
import zipfile
import openpyxl
from openpyxl.drawing.image import Image
import shutil


def add_image(path_src, path_file):
    path_image = "C:/Users/liang-jiashun/Desktop/Excel模板/image"
    shutil.rmtree(path_image)
    os.makedirs(path_image)
    files = os.listdir(path_src)  # 文件遍历
    for file in files:
        if file != "test":
            shutil.copy(path_src+"/"+file, path_image)

    wb = openpyxl.load_workbook(filename=path_file)
    ws = wb.worksheets[0]
    ws1 = wb.worksheets[1]
    files = os.listdir(path_image)           # 文件遍历
    index = 4
    for file in files:
        if not os.path.isdir(path_image + "/" + file):
            file_name = os.path.basename(path_image + "/" + file)  # 获取文件名
            new_name = str(file_name.split('.')[0]) + ".zip"  # 新的文件名，命名为：xxx.zip
            dir_path = os.path.dirname(path_image + "/" + file)  # 获取文件所在目录
            new_path = dir_path+"/"+new_name  # 新的文件路径
            os.rename(path_image + "/" + file, new_path)

            file_zip = zipfile.ZipFile(new_path, 'r')
            zipdir = path_image+"/"+str(file.split('.')[0])  # 获取文件所在目录
            for files in file_zip.namelist():
                file_zip.extract(files, zipdir)  # 解压到指定文件目录
            file_zip.close()
            os.remove(new_path)

            pic_dir = 'xl'+"/"+'media'  # excel变成压缩包后，再解压，图片在media目录
            pic_path = path_image+"/"+str(file.split('.')[0])+"/"+pic_dir
            image = pic_path + "/" +"image1.jpeg"

            print(image)
            ws.column_dimensions['A'].width = 9.1
            ws.row_dimensions[index].height = 57
            ws1.column_dimensions['A'].width = 9.1
            ws1.row_dimensions[index].height = 57
            img1 = Image(image)
            img2 = Image(image)
            img1.width, img1.height = 73, 73
            img2.width, img2.height = 73, 73
            ws.add_image(img1,'A'+str(index))
            ws1.add_image(img2, 'A' + str(index))
            index += 1
            wb.save(filename=path_file)
    wb.close()
