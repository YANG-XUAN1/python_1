#-*- coding: UTF-8 -*-
# @程序作者：NEW蓝
# @功能描述：ts
# @Time : 2021/12/10 20:41
import sys

import shapefile
import json
import arcpy
import numpy as np


# 获取每个泰森多边形的面积
def polygon_area(lis):
    sizep = len(lis)
    if sizep<3:
        return 0.0
    area = lis[-1][0] * lis[0][1] - lis[0][0] * lis[-1][1]

    for i in range(1,sizep):
        v = i - 1
        area += (lis[v][0] * lis[i][1])
        area -= (lis[i][0] * lis[v][1])
    return abs(0.5 * area)


# 生成泰森多边形
def createTaiSen(inputpath, outputPath):
    arcpy.CreateThiessenPolygons_analysis(inputpath, outputPath, "ALL")

# 处理泰森多边形数据
def deal_TaiSen(inputPath):
    # 新建字典保存数据
    r = shapefile.Reader(inputPath)
    fields = r.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in r.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geomtry = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geomtry, properties=atr))

    jsonData = json.dumps({"type": "FeatureCollection", "features": buffer}, indent=4)
    areaList = []
    # 求每个多边形的面积
    dictData = json.loads(jsonData)['features']
    for i in dictData:
        nearList = []
        data = np.array(i["geometry"]["coordinates"][0][:-1][::-1])
        area = polygon_area(data)
        id = i["properties"]["OBJECTID"]
        for ii in json.loads(jsonData)["features"]:
            if ii != i:
                for iii in ii["geometry"]["coordinates"][0]:
                    if iii in i["geometry"]["coordinates"][0]:
                        nearList.append(ii["properties"]["OBJECTID"])
                        break
        areaList.append([id, area, nearList])

    tempList = sorted(areaList, key=lambda x:x[1])
    return tempList    #[点的id, 点的权重, 点的临界点]


#初始化数组，自由——0
def start_array(inputfile):
    location = []  # 导入数据数组
    r = shapefile.Reader(inputfile)  # 导入数据路径
    for i in r.iterShapeRecords():
        ii = i.record
        location.append([ii[3], ii[4],0])
    r.close()
    return location


#改变点类型是“固定”——2、“被删”——1、“自由”——0
def change_type(ts,data):
    print(len(data))
    print(len(ts))
    for i in ts:
        loca = []
        for l in i[2]:
            loca.append(data[l-1])
        k = len(i)    #
        for j in loca:
            if j[2] == 0:
                k -= 1
        if k == 0:
            # poi = data[i[0]]
            data[i[0]][2] = 1
            for l in i[2]:
                data[l-1][2] = 2
            del i
    return ts,data


#新建图层信息
def new_shp(data,inputfile,outputfile):
    # inputfile = "E:\\new\\points\\points.shp"
    r = shapefile.Reader(inputfile)
    w = shapefile.Writer(outputfile,shapeType=r.shapeType)
    w.fields = list(r.fields)
    d = 0
    j = 0
    for i in r.iterShapeRecords():
        ls = i.record
        if data[d][2] != 1:
            d += 1
            ls[0] = j    #每行编号
            j += 1
            w.record(*ls)
            w.shape(i.shape)
            # print(ls)
            continue
        d += 1
    w.close()
    r.close()


# 参数为：第几次遍历,定义createTaiSen()的输入路径,定义多边形的输出路径,原数据总长度
def circulation(count,inputPath,outputPath,l):
    createTaiSen(inputPath, outputPath)     # 处理数据

    ts = deal_TaiSen(outputPath)            # 处理完数组,获取处理完数组
    location = start_array(inputPath)       # 初始化点数据

    ts, location = change_type(ts, location)     #删除数据
    i = str(count)
    outputfile = "E:\\new\\points\\point" + i + ".shp"         # 定义新建图层的输出路径
    new_shp(location, inputPath,outputfile)                       #导出数据

    if len(ts) > (l/2):
        outputfile2 = "E:\\new\\taisen" + i
        count += 1
        circulation(count, outputfile, outputfile2, l=l)

    return 0


#主函数
def main():
    count = 1
    inputPath = "E:\\new\\points\\points.shp"       #定义createTaiSen()的输入路径
    outputPath = "E:\\new\\points_new"              #定义多边形的输出路径
    createTaiSen(inputPath, outputPath)             # 处理数据,建立泰森多边形
    ts = deal_TaiSen(outputPath)                    # 处理完数组,获取泰森多边形数组
    location = start_array(inputPath)               # 初始化点数据
    length = len(location)                          #定义初始总长度

    ts, location = change_type(ts, location)     #第一次删除数据
    i = str(count)
    outputfile = "E:\\new\\points\\point" + i + ".shp"
    new_shp(location, inputPath,outputfile)                       #导出数据
    if len(ts) > (length / 2):
        outputfile2 = "E:\\new\\taisen" + i
        count += 1
        circulation(count, outputfile, outputfile2, l=length)
    return 0


if __name__ == '__main__':
    main()
