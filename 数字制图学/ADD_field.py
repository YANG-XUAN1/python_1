# -*- coding：utf-8 -*-
# @程序作者：NEW蓝
# @功能描述：ADD_field
# @Time : 2021/11/27 16:00
import shapefile
import json

# r = shapefile.Reader(r"E:\数字制图原理实习\coverage\B\POG.shp")
# w = shapefile.Writer(r"E:\数字制图原理实习\coverage\B\POG_update.shp",
#                      shapeType=r.shapeType)
# w.fields = list(r.fields)
# # 新增加两个字段
# w.field("LAT", "F", 8, 5)
# # w.field("LON", "F", 8, 5)
#
# # 将另外一个文件中的坐标点的信息存入新增加的两个字段
# # geo = shapefile.Reader(r"E:\数字制图原理实习\coverage\B\polygon_property.txt")
# f = open(r"E:\数字制图原理实习\coverage\B\polygon_property.txt")
# geo = f.readlines()
# i = 0
# # print(r.iterShapeRecords())
# for rec in r.iterShapeRecords():
#     ls = rec.record
#     lon = geo[i]  # 可以再此处增加判断语句，限制i的大小。防止增加的字段数目不匹配问题
#     # print(geo.shape(i).points)
#     ls.extend([lon])
#     # print(ls)
#     w.record(*ls)
#     w.shape(rec.shape)
#     i += 1
#
# w.close()



def add_field(coverage,name,propertyfile):
    infile = f"E:\\数字制图原理实习\\coverage\\{coverage}\\{name}.shp"
    outfile = f"E:\\数字制图原理实习\\coverage\\{coverage}\\{name}_Update.shp"
    r = shapefile.Reader(fr"{infile}")
    w = shapefile.Writer(fr"{outfile}",shapeType=r.shapeType)
    w.fields = list(r.fields)
    # 新增加两个字段
    w.field("property", "F", 8, 5)
    # 将另外一个文件中的坐标点的信息存入新增加的两个字段
    propertyfile = f"E:\\数字制图原理实习\\coverage\\{coverage}\\{propertyfile}_property.txt"
    f = open(fr"{propertyfile}")
    geo = f.readlines()
    i = 0
    for rec in r.iterShapeRecords():
        ls = rec.record
        lon = geo[i]  # 可以再此处增加判断语句，限制i的大小。防止增加的字段数目不匹配问题
        # print(geo.shape(i).points)
        ls.extend([lon])
        # print(ls)
        w.record(*ls)
        w.shape(rec.shape)
        i += 1

    w.close()

if __name__ == '__main__':
    with open("E:\数字制图原理实习\coverage\json.txt",mode='r') as f:
        text = f.read()
        print(text)
        updata = json.loads(text)
        for i in updata:
            for j in i:
                coverage = j
                proper = i[j]
                if proper == "Point":
                    name = "POI"
                if proper == "Polylines":
                    name = "POL"
                if proper == "Polygon":
                    name = "POG"
                # print(coverage,name,proper)
                add_field(coverage,name,proper)

