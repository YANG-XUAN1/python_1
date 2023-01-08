# -*- coding：utf-8 -*-
# @程序作者：NEW蓝
# @功能描述：split
# @Time : 2021/11/26 14:02

import json




data = []
coverage =[]
index = []
ind = 0
form = ['Point','Polyline','Polygon']
update = []

f = open("E:\数字制图原理实习\data.txt",mode='r',encoding='utf-8')
for d in f:
    da = d.strip('\n').replace(',','')
    if 'A'<da<'Z' and len(da) == 1:
        coverage.append(da)  #保存层号
        # print(ind)
        index.append(ind)    #保存每层起始点
    da = da.split(' ')
    # print(da)
    data.append(da)
    ind = ind + 1
    # data.append(d.strip('\n').strip(' ').split(','))
f.close()
index.append(ind)
# print(coverage)

dire = 0
for i in range(len(index)-1):
        dat = data[index[i]+1:index[i + 1]]   #每层数据
        for i in dat:

            if i[0] == form[0]:     #点数据
                num = eval(i[1])
                dict_poi = {}
                if num != 0:        #判断是否存在点数据
                    id = coverage[dire]
                    dict_poi[f"{id}"] = "Point"
                    update.append(dict_poi)
                    with open(f"E:\\数字制图原理实习\\coverage\\{coverage[dire]}\\Point.txt", mode='w') as f:
                        with open(f"E:\\数字制图原理实习\\coverage\\{coverage[dire]}\\point_property.txt", mode='w') as f2:
                            f.write("Point" + '\n')
                            property = []
                            pro = 0
                            c = dat.index(i)
                            for j in range(num*2):
                                if len(dat[c+j+1]) == 1:     #属性码
                                    property.append(dat[c+j+1])
                                if len(dat[c+j+1]) == 2:     #输出数据
                                    f2.write(property[pro][0] + "\n")
                                    f.write(f"{pro+1}" + " " + dat[c+j+1][0] + " " + dat[c+j+1][1]  + "\n")
                                    pro = pro + 1
                            f.write("END" + "\n")


            if i[0] == form[1]:     #线数据
                num = eval(i[1])    # 线的数目
                dict_line = {}
                if num != 0:        #判断是否存在线数据
                    id = coverage[dire]
                    dict_line[f"{id}"] = "Polylines"
                    update.append(dict_line)
                    with open(f"E:\\数字制图原理实习\\coverage\\{coverage[dire]}\\Polylines.txt", mode='w') as f:
                        with open(f"E:\\数字制图原理实习\\coverage\\{coverage[dire]}\\polylines_property.txt", mode='w') as f2:
                            f.write("Polyline" + '\n')
                            property = []
                            pro = 0
                            c = dat.index(i)
                            oid = 1
                            for j in range(num):
                                property.append(dat[c+1])   #属性码
                                t = eval(dat[c+2][0])       #线中点的数目
                                f.write(f"{oid}" + " " + "0" + "\n")
                                f2.write(str(dat[c+1][0]) + "\n")
                                oid = oid + 1
                                poi = 0
                                for m in range(1,t+1):
                                    f.write(f"{poi}" + " " + dat[c + m + 2][0] + " " + dat[c + m + 2][1]  + "\n")
                                    poi = poi +1
                                pro = pro + 1
                                c = t + 3 + c
                            f.write("END" + "\n")

            if i[0] == form[2]:         #面数据
                num = eval(i[1])        # 面的数目
                dict_pog = {}
                if num != 0:            #判断是否存在面数据
                    id = coverage[dire]
                    dict_pog[f"{id}"] = "Polygon"
                    update.append(dict_pog)
                    with open(f"E:\\数字制图原理实习\\coverage\\{coverage[dire]}\\Polygon.txt", mode='w') as f:
                        with open(f"E:\\数字制图原理实习\\coverage\\{coverage[dire]}\\polygon_property.txt", mode='w') as f2:
                            f.write("Polygon" + "\n")
                            c = dat.index(i)
                            oid = 1
                            for j in range(num):
                                property.append(dat[c + 1])     # 属性码
                                t = eval(dat[c + 2][0])         # 面中点的数目
                                f.write(f"{oid}" + " " + "0" + "\n")
                                f2.write(str(dat[c + 1][0]) + "\n")
                                oid =oid+1
                                point = 0
                                for m in range(1, t + 1):
                                    f.write(f"{point}" + " " + dat[c + m + 2][0] + " " + dat[c + m + 2][1]  + "\n")
                                    point=point+1
                                pro = pro + 1
                                c = t + 3 + c
                            f.write("END" + "\n")
        dire = dire + 1

print(update)
text = json.dumps(update,ensure_ascii=False)
print(text)
with open("E:\数字制图原理实习\coverage\json.txt",mode="w") as f:
    f.write(text)



