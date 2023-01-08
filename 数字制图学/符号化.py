# -*- coding：utf-8 -*-
# @程序作者：NEW蓝
# @功能描述：符号化
# @Time : 2021/11/30 9:03

import shapefile
import json

C = []
B = []
P=[]
V=[]
R=[]
T=[]
H=[]
F=[]
coverages = ["V","C","P","B","F","H","T","R"]
with open("E:\数字制图原理实习\code.txt",mode='r') as f:
    data = f.readlines()
    for i in data:
        j = i.strip('\n').split("      ")
        ii = j[2]
        if ii == 'C':
            C.append([float(j[0]),j[3]])
        if ii == 'B':
            B.append([float(j[0]),j[3]])
        if ii == 'P':
            P.append([float(j[0]),j[3]])
        if ii == 'V':
            V.append([float(j[0]),j[3]])
        if ii == 'T':
            T.append([float(j[0]),j[3]])
        if ii == 'R':
            R.append([float(j[0]),j[3]])
        if ii == 'H':
            H.append([float(j[0]),j[3]])
        if ii == 'F':
            F.append([float(j[0]),j[3]])

# print(C,
# B ,
# P,
# V,
# R,
# T,
# H,
# F)


def selectname(pro):   #转换name
    if pro == "Point":
        name = "POI"
    if pro == "Polylines":
        name = "POL"
    if pro == "Polygon":
        name = "POG"
    return name

def add_field(coverage,name,lis):     #根据属性值添加地物类型
    infile = f"E:\\数字制图原理实习\\coverage\\{coverage}\\{name}_Update.shp"
    outfile = f"E:\\数字制图原理实习\\coverage\\{coverage}\\{name}_Add.shp"
    print(coverage,name)
    r = shapefile.Reader(fr"{infile}")
    w = shapefile.Writer(fr"{outfile}",shapeType=r.shapeType,encoding='gbk')
    w.fields = list(r.fields)
    # 新增加一个字段
    w.field("form", "C", 100,100)
    for rec in r.iterShapeRecords():
        ls = rec.record
        for fm in lis:
            if ls[2] == fm[0]:
                # print(ls[2])
                form = fm[1]
                print(form)
                ls.extend([form])
                w.record(*ls)
                w.shape(rec.shape)
                print(ls)
                break
    w.close()

def selectCov(coverage,pro):
    if coverage == "B":
        name = selectname(pro)
        add_field(coverage,name,B)
    if coverage == "P":
        name = selectname(pro)
        add_field(coverage,name,P)
    if coverage == "T":
        name = selectname(pro)
        add_field(coverage,name,T)
    if coverage == "V":
        name = selectname(pro)
        add_field(coverage,name,V)
    if coverage == "C":
        name = selectname(pro)
        add_field(coverage,name,C)
    if coverage == "R":
        name = selectname(pro)
        add_field(coverage,name,R)
    if coverage == "H":
        name = selectname(pro)
        add_field(coverage,name,H)
    if coverage == "F":
        name = selectname(pro)
        add_field(coverage,name,F)

def main():
    with open("E:\数字制图原理实习\coverage\json.txt",mode='r') as f:
        text = f.read()
        # print(text)
        updata = json.loads(text)
        for i in updata:
            for j in i:
                coverage = j
                proper = i[j]
                selectCov(coverage,proper)




if __name__ == '__main__':
    main()
