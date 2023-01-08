# -*- coding：utf-8 -*-
# @程序作者：NEW蓝
# @功能描述：K_mean
# @Time : 2021/12/9 21:52
import shapefile
import random
import math
import numpy as np

#求两点间距离
def distance(p1,p2):
    # print(p1,p2)
    return math.sqrt((math.pow(p1[0]-p2[0],2)+math.pow(p1[1]-p2[1],2)))

#求新的聚类中心
def new_centers(arr):
    arr1 = []
    arr2 = []
    for j in arr:
        arr1.append(j[0])
        arr2.append(j[1])
    x = y = 0
    for a in arr1:      #新的聚类中心坐标
        x += a[0]
        y += a[1]
    l = len(arr)
    X = x/l
    Y = y/l

    arr2 = np.sort(arr2)
    if l % 2 == 0:          #新的中心面积/长度
        c = int(l/2)
        c2 = int((l/2)-1)
        cent = (arr2[c] + arr2[c2])/2
    else:
        c = int((l-1)/2)
        cent = arr2[c]

    return [[X,Y],cent]


#K均值函数
def k_mean(data,centers):
    first = []
    first.append(centers[0])        #将每个聚类中心放入对应的数组
    second = []
    second.append(centers[1])
    third = []
    third.append(centers[2])
    forth = []
    forth.append(centers[3])

    for d in data:
        d_xy = d[0]                      #每个点的坐标
        compare = []
        for c in centers:                #求每个点到聚类中心的聚类
            c_xy = c[0]                  #聚类中心点坐标
            dis = distance(d_xy, c_xy)         #两点间距离
            if abs(d[1] - c[1]) > 1.5:
                dis = dis * 10
            compare.append(dis)
        index = compare.index(np.min(compare))          #求最小距离为那个聚类中心
        #选择将点放入哪个聚类中
        if index == 0:
            first.append(d)
        elif index == 1:
            second.append(d)
        elif index == 2:
            third.append(d)
        else:
            forth.append(d)
    #新的聚类中心
    c0 = new_centers(first)
    c1 = new_centers(second)
    c2 = new_centers(third)
    c3 = new_centers(forth)
    if (distance(c0[0],centers[0][0]) > 0.1) or (distance(c1[0],centers[1][0]) > 0.1) or \
            (distance(c2[0],centers[2][0]) > 0.1) or (distance(c3[0],centers[3][0]) > 0.1):
        centers = [c0,c1,c2,c3]
        print(centers)
        k_mean(data,centers)

    return first,second,third,forth

def main():
    r = shapefile.Reader("E:\数字制图-课程设计\数据\实习3\\buildings")  #打开文件
    data = []
    for i in r.iterShapeRecords():
        j= i.record
        data.append([[j[-2],j[-1]],j[3]/j[2]])     #保存点数据(坐标，面积长度比)

    centers = random.sample(data,4)   #初始化4个质心

    first,second,third,forth = k_mean(data,centers)    #求聚类和每个聚类的新质心

    for d in data:              #判断类别
        if d in first:
            d.extend([1])
        elif d in second:
            d.extend([2])
        elif d in third:
            d.extend([3])
        else:
            d.extend([4])
        # print(d)

    w = shapefile.Writer("E:\数字制图-课程设计\数据\实习3\\new_buildings",shapeType=r.shapeType)  #导出文件
    w.fields = list(r.fields)
    w.field("class","C",20)
    for rec in r.iterShapeRecords():
        ls = rec.record
        for d in data:
            dat = d[0]
            if ls[-2] == dat[0] and ls[-1] == dat[1]:
                lon = d[2]
                ls.extend([lon])
                # print(ls)
                w.record(*ls)
                w.shape(rec.shape)
                break

    w.close()
    r.close()

if __name__ == '__main__':
    main()








