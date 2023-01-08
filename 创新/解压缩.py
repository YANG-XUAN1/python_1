# -*- coding：utf-8 -*-
# @程序作者：NEW蓝
# @功能描述：解压缩
# @Time : 2022/1/12 8:52

import zipfile
import os
list = ['01','02','03','04','05','06','07','08','09','10','11','12']
sen2cor_path = r"E:\创新实验数据\Sen2Cor-02.08.00-win64\L2A_Process.bat"
pattern = ".SAFE"
for l in list:
    origin_dir = fr"F:\Sentinel-2\2019\{l}"
    for zip_file in os.listdir(origin_dir):
        print(zip_file)