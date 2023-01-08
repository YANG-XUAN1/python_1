# -*- coding：utf-8 -*-
# @程序作者：NEW蓝
# @功能描述：cen2cor
# @Time : 2022/1/11 10:43

import subprocess
import zipfile
import os

#'01','02','03','04','05','06','07','08','09','10','11','12'
# '2','3','4','5','6','7','8','9','10','11','12'
list = ['10','11','12']
Sentienal_Time = ["2018_10","2019_6","2019_03","2019_11"]
sen2cor_path = "E:\创新实验数据\Sen2Cor-02.08.00-win64\L2A_Process.bat"
# sen2cor255_path = "E:\创新实验数据\Sen2Cor-02.05.05-win64\L2A_Process.bat"
pattern = ".SAFE"
count = 0
# for l in list:
#     origin_dir = fr"F:\Sentinel-2\2017\{l}"
for S in Sentienal_Time:
    origin_dir = fr"F:\Sentinel-2\{S}"
    # print(origin_dir)
    for in_file in os.listdir(origin_dir):
        if len(in_file.split(".")) == 2:
            continue
        else :
            # if in_file.startswith("S2A"):
            #     # print(in_file)
            #     zip_file_path = os.path.join(origin_dir,in_file)
            #     # print(zip_file_path)
            #     for SAFE_file in os.listdir(zip_file_path):
            #         xml_file_path = os.path.join(zip_file_path,SAFE_file)
            #         # print(xml_file_path)
            #         os.chdir(xml_file_path)
            #         cmd_args = [sen2cor255_path,xml_file_path]
            #         print(count,":",cmd_args)
            #         count += 1
            #

            #         # subprocess.call(cmd_args)
            #
            # else:
            #     # print("L:",in_file)
            #     zip_file_path = os.path.join(origin_dir, in_file)
            #     # print(zip_file_path)
            #     for SAFE_file in os.listdir(zip_file_path):
            #         xml_file_path = os.path.join(zip_file_path,SAFE_file)
            #         # print(xml_file_path)
            #         os.chdir(xml_file_path)
            #         cmd_args = [sen2cor255_path, xml_file_path]
            #         print(count, ":", cmd_args)
            #         count += 1
            #
            #         subprocess.call(cmd_args)


            zip_file_path = os.path.join(origin_dir, in_file)
            # print(zip_file_path)
            for input_file in os.listdir(zip_file_path):
                xml_file_path = os.path.join(zip_file_path, input_file)
                # print(xml_file_path)
                os.chdir(xml_file_path)
                # print(os.getcwd())
                cmd_args = [sen2cor_path, xml_file_path]
                print(count,":",cmd_args)
            #     #
                subprocess.call(cmd_args)
                count += 1



