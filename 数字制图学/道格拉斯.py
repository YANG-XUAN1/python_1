# -*- coding：utf-8 -*-
# @程序作者：NEW蓝
# @功能描述：道格拉斯
# @Time : 2021/12/2 15:05
import math
from shapely import wkt, geometry
import matplotlib.pyplot as plt


Lines = []
Gons = []
data = []
coverage =[]
index = []
ind = 0
form = ['Point','Polyline','Polygon']

f = open("E:\数字制图原理实习\data.txt",mode='r',encoding='utf-8')
for d in f:
    da = d.strip('\n').replace(',','')
    if 'A'<da<'Z' and len(da) == 1:
        coverage.append(da)  #保存层号
        index.append(ind)    #保存每层起始点
    da = da.split(' ')
    data.append(da)
    ind = ind + 1
f.close()
index.append(ind)

dire = 0
for i in range(len(index)-1):
        dat = data[index[i]+1:index[i + 1]]   #每层数据
        for i in dat:

            if i[0] == form[1]:     #线数据
                num = eval(i[1])    # 线的数目
                if num != 0:        #判断是否存在线数据
                    id = coverage[dire]
                    # property = []
                    c = dat.index(i)
                    # oid = 1
                    for j in range(num):
                        line = []
                        t = eval(dat[c+2][0])       #线中点的数目
                        # oid = oid + 1
                        poi = 0
                        for m in range(1,t+1):
                            line.append([dat[c + m + 2][0] ,dat[c + m + 2][1]])
                        Lines.append(line)
                        c = t + 3 + c


            if i[0] == form[2]:         #面数据
                num = eval(i[1])        # 面的数目
                dict_pog = {}
                if num != 0:            #判断是否存在面数据
                    id = coverage[dire]
                    pro = 0
                    c = dat.index(i)
                    for j in range(num):
                        gon = []
                        t = eval(dat[c + 2][0])         # 面中点的数目
                        point = 0
                        for m in range(1, t + 1):
                            gon.append([dat[c + m + 2][0] , dat[c + m + 2][1]])
                        Gons.append(gon)
                        c = t + 3 + c
        dire = dire + 1

# print(Gons)
# print(Lines)


class Point:
    """点类"""
    x = 0.0
    y = 0.0
    index = 0  # 点在线上的索引

    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index


class Douglas:
    """道格拉斯算法类"""
    points = []
    D = 0.1  # 容差

    def readPoint(self):
        """生成点要素"""
        # g = wkt.loads("LINESTRING(96971 49511, 96965 49510, 96964 49511, 96971 49511)")
        g = wkt.loads(f"LINESTRING(1 8,2 3,4 3,6 6,7 7,8 6,9 5,10 10)")
        coords = g.coords
        for i in range(len(coords)):
            self.points.append(Point(coords[i][0], coords[i][1], i))

    def compress(self, p1, p2):        #具体的道格拉斯算法
        swichvalue = False
        # 一般式直线方程系数 A*x+B*y+C=0,利用点斜式,分母可以省略约区
        A = (p1.y - p2.y)
        B = (p2.x - p1.x)
        C = (p1.x * p2.y - p2.x * p1.y)
        m = self.points.index(p1)
        n = self.points.index(p2)
        distance = []
        middle = None

        if (n == m + 1):
            return
        # 计算中间点到直线的距离
        for i in range(m + 1, n):
            d = abs(A * self.points[i].x + B * self.points[i].y + C) / math.sqrt(math.pow(A, 2) + math.pow(B, 2))
            distance.append(d)
        dmax = max(distance)

        if dmax > self.D:
            swichvalue = True
        else:
            swichvalue = False

        if (not swichvalue):
            for i in range(m + 1, n):
                del self.points[i]
        else:
            for i in range(m + 1, n):
                if (abs(A * self.points[i].x + B * self.points[i].y + C) / math.sqrt(
                        math.pow(A, 2) + math.pow(B, 2)) == dmax):
                    middle = self.points[i]
            self.compress(p1, middle)
            self.compress(middle, p2)

    def printPoint(self):
        """打印数据点"""
        for p in self.points:
            print("%d,%f,%f"%(p.index, p.x, p.y))


def main():
    """测试"""

    d = Douglas()
    d.readPoint()
    # d.printPoint()
    # 结果图形的绘制，抽稀之前绘制
    fig = plt.figure()
    a1 = fig.add_subplot(121)
    dx = []
    dy = []
    for i in range(len(d.points)):
        dx.append(d.points[i].x)
        dy.append(d.points[i].y)
    a1.plot(dx, dy, color='g', linestyle='-', marker='+')

    d.compress(d.points[0], d.points[len(d.points) - 1])

    # 抽稀之后绘制
    dx1 = []
    dy1 = []
    a2 = fig.add_subplot(122)
    for p in d.points:
        dx1.append(p.x)
        dy1.append(p.y)
    a2.plot(dx1, dy1, color='r', linestyle='-', marker='+')

    print ("========================\n")
    d.printPoint()
    plt.show()


if __name__ == '__main__':
    main()
