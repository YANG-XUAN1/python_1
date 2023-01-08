# -*- coding：utf-8 -*-
# @程序作者：NEW蓝
# @功能描述：Voronoi
# @Time : 2021/12/3 16:31
# import shapefile
# import matplotlib.pyplot as plt
# import numpy as np
# import math

# class voronoi:
#     voronoi_p = []
#     def __init__(self,name):
#         self.name = name
#
#
#     #求两点间距离
#     def distance(self,a,b):
#         dist = pow(a[0]-b[0],2) + pow(a[1]-b[1],2)
#         d = math.sqrt(dist)
#         return d
#
#
#     #求最小距离点
#     def minpoint(self,location):
#         dist = []
#         voi = voronoi("")
#         p1 = location[0]
#         for i in location:
#             if i !=p1:
#                 d = voi.distance(p1,i)
#                 dist.append(d)
#                 if d == np.min(dist):
#                     min = d             #最小距离的值
#                     dist.append(min)
#                     p2 = i              #最小距离点
#         return p1,p2
#
#
#     #求角度
#     def trangle(self,p1,p2,p3):
#         p12 = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
#         p13 = math.sqrt((p1[0]-p3[0])**2 + (p1[1]-p3[1])**2)
#         p23 = math.sqrt((p3[0]-p2[0])**2 + (p3[1]-p2[1])**2)
#         cos = (p13**2+p23**2-p12**2)/(2*p13*p23)
#         return cos
#
#
#     #右侧最大角度
#     def max_right_angle(self,p1,p2,location):
#         voi = voronoi("")
#         Q = []
#         angle = []
#         p3 =[]
#         A = p2[1]-p1[1]              #一般方程系数
#         B = p2[0]-p1[0]
#         C = p2[0]*p1[1]-p1[0]*p2[1]
#         for p in location:
#             if p!=p1 and p!=p2:
#                 if A*p[0] + B*p[1] + C > 0:
#                     cos = voi.trangle(p1, p2, p)
#                     angle.append(cos)
#                     if cos == np.min(angle):
#                         p3 = p
#         if p3 != []:
#             if [p1,p3]not in voi.voronoi_p :
#                 voi.voronoi_p.append([p1, p3])
#                 Q.append([p1, p3])
#                 if [p3,p2] not in voi.voronoi_p:
#                     voi.voronoi_p.append([p3, p2])
#                     Q.append([p3, p2])
#                     return Q
#                 else:
#                     return Q
#             else:
#                 return Q
#
#
#     #求第一次Q
#     def voronio_Q(self,location,Q):
#         voi = voronoi("")
#         # Q = []
#         # p,p0 = voi.minpoint(location)
#         # Q.append([p,p0])
#         # Q.append([p0,p])
#         if Q :
#             for q in Q:
#                 p1 = q[0]
#                 p2 = q[1]
#                 # print(p1,p2)
#                 Q1 = voi.max_right_angle(p1,p2,location)
#                 voi.voronio_Q(location,Q1)
#                 # if p3 in location:
#                 #     if [p1, p3] not in Q:
#                 #         Q.append([p1, p3])
#                 #     if [p3,p1] not in Q:
#                 #         Q.append([p3, p2])
#         # p4 = voi.max_left_angle(p1,p2,location)
#         # p4 = voi.max_right_angle(p2,p1,location)
#         # if p4 in location:
#         #     Q.append([p2,p4])
#         #     Q.append([p4,p1])
#         # print(voi.voronoi_p)
#         return voi.voronoi_p
#
#     #
# def main():
#     location = []
#     r = shapefile.Reader("E:\数字制图-课程设计\数据\实习1\points.shp")
#     for i in r.iterShapeRecords():
#         ii = i.record
#         location.append([ii[3], ii[4]])
#     r.close()
#
#     vor = voronoi("")
#     p1,p2 = vor.minpoint(location)
#     Q = vor.max_right_angle(p1,p2,location)
#     # print(Q)
#
#     voron = vor.voronio_Q(location,Q)
#
#     return voron
#
#
# if __name__ == '__main__':
#     voron = main()
#     print(voron)





import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import shapefile

def circumcenter(triangle):           #求外心
    triangle = np.array(triangle,dtype=np.float64)
    x1 = triangle[0][0]
    y1 = triangle[0][1]
    x2 = triangle[1][0]
    y2 = triangle[1][1]
    x3 = triangle[2][0]
    y3 = triangle[2][1]
    # print(x1,y1)
    a1 = 2 * (x2 - x1)
    b1 = 2 * (y2 - y1)
    c1 = x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1
    #
    a2 = 2 * (x3 - x2)
    b2 = 2 * (y3 - y2)
    c2 = x3 * x3 + y3 * y3 - x2 * x2 - y2 * y2
    #
    x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
    y = (a1 * c2 - a2 * c1) / (a1 * b2 - a2 * b1)
    return [x,y]


# def intersection(triangle,center):
#     x12 = (triangle[0][0] + triangle[1][0])/2
#     y12 = (triangle[0][1] + triangle[1][1])/2
#     x23 = (triangle[1][0] + triangle[2][0])/2
#     y23 = (triangle[1][1] + triangle[2][1])/2
#     x31 = (triangle[2][0] + triangle[0][0])/2
#     y31 = (triangle[2][1] + triangle[0][1])/2
#     x = center[0]
#     y = center[1]
#     A12 = (x - x12)/(y - y12)
#     A23 = (x - x23) / (y - y23)
#     A31 = (x - x31) / (y - y31)
#     y =




def triangle_area(lis):     #计算面积
    sizep = len(lis)
    if sizep<3:
        return 0.0
    area = lis[-1][0] * lis[0][1] - lis[0][0] * lis[-1][1]

    for i in range(1,sizep):
        v = i - 1
        area += (lis[v][0] * lis[i][1])
        area -= (lis[i][0] * lis[v][1])
    return abs(0.5 * area)


location = []                                                           #导入数据数组
r = shapefile.Reader("E:\数字制图-课程设计\数据\实习1\points.shp")        #导入数据路径
for i in r.iterShapeRecords():
    ii = i.record
    location.append([ii[3], ii[4]])
r.close()

points = np.array(location)             #将数组转换为array
tri = Delaunay(points)                    # 三角剖分
# print(points)
plt.triplot(points[:,0], points[:,1], tri.simplices.copy())        #画三角剖分 图
plt.plot(points[:,0], points[:,1], 'o')
plt.show()
plt.savefig("voronoi")


points_index = tri.simplices                # 每个三角面对应的点的索引index
points_vertex = points[tri.simplices]       # 每个三角面所包含的坐标点
le = len(points)
# print(points_vertex)
print(points_index)

points_voronoi = []         #每个顶点所在的三角形
for i in range(0,le):
    near = []
    near.append(i)
    for ver in points_index:
        # if i == ver[0] or i ==ver[1] or i == ver[2]:
        if i in ver:
            near.append(ver)
            continue
    points_voronoi.append(near)

for poi in points_voronoi:         #将顶点的index转换为坐标
    for i in range(len(poi)):
        poi[i] = points[poi[i]]
    # poi[1] = points[poi[1]]
    # poi[2] = points[poi[2]]
    # poi[3] = points[poi[3]]
del poi
# print(points_voronoi)

S = []          #每个多边形的面积 ,及顶点
area = []       #每个多边形的面积
for poi in points_voronoi:        #求每个三角形外心
    for p in range(len(poi)):
        if len(poi[p]) == 3:
            center = circumcenter(poi[p])
            if 12959795.046600 > center[0] > 12958841.124000 or 4856068.164600 < center[1] < 4854798.300500:
                x1 = poi[p][0][0]
                y1 = poi[p][0][1]
                x2 = poi[p][1][0]
                y2 = poi[p][1][1]
                x3 = poi[p][2][0]
                y3 = poi[p][2][1]
            poi[p] = center

del poi
# print(points_voronoi)

# print(type([12959033.210875332, 4856198.176392573]))
for poi in points_voronoi:
    lis = []
    for p in range(len(poi)):
        if type(poi[p]) == list:
            lis.append(poi[p])
        else:continue
    # print(lis)
    s = triangle_area(lis)
    S.append([poi[0],s])
    area.append(s)
print(area)
area.sort()




# sim = np.array(points_vertex,dtype=np.float64)
# circle = []
# circum_center = []
# for c in sim:             #外心
#     x1 = c[0][0]
#     y1 = c[0][1]
#     x2 = c[1][0]
#     y2 = c[1][1]
#     x3 = c[2][0]
#     y3 = c[2][1]
#     # print(x1,y1)
#
#     a1 = 2 * (x2 - x1)
#     b1 = 2 * (y2 - y1)
#     c1 = x2 * x2 + y2 * y2 - x1 * x1 - y1 * y1
#
#     a2 = 2 * (x3 - x2)
#     b2 = 2 * (y3 - y2)
#     c2 = x3 * x3 + y3 * y3 - x2 * x2 - y2 * y2
#
#     x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
#     y = (a1 * c2 - a2 * c1) / (a1 * b2 - a2 * b1)
#     # print(x,y)
#     # if 12959795.046600>x>12958841.124000 or 4856068.164600<y<4854798.300500:
#
#     # xy = np.array([x,y])
#     # circle.append([["{:.8f}".format(x1),"{:.8f}".format(y1)],["{:.8f}".format(x2),"{:.8f}".format(y2)],["{:.8f}".format(x3),"{:.8f}".format(y3)],["{:.8f}".format(x),"{:.8f}".format(y)]])
#     circle.append([[x1,y1],[x2,y2],[x3,y3],[x,y]])
#     circum_center.append([x,y])
#
#
# voronoi = []
# for cir in circle:     #相同边的外心
#     a = cir[0]
#     b = cir[1]
#     c = cir[2]
#     for cir2 in circle:
#         if cir != cir2:
#             if ((a in cir2) and (b in cir2 )) or ((c in cir2 )and (b in cir2 )) or ((a in cir2) and (c in cir2 )):
#                 voronoi.append([cir[3],cir2[3]])


def find(a,list):
    fin = []
    fin.append(a)
    for l in list:
        t = l
        if a[1] == l[0]:
            a = t
            f = find(a,list)
            fin.append(f)
    return fin

# voronoi_shape = []
# for v in voronoi:
#     fi = find(v,voronoi)
#     voronoi_shape.append(fi)

# voronoi = np.array(voronoi,dtype=np.float64)
# circum_center = np.array(circum_center)
# voronoi_shape = np.array(voronoi,np.float64)

#画图
# plt.xlim(12958841.124000,12959795.046600)
# plt.ylim(4856068.164600,4854798.300500)
# plt.triplot(circum_center[:,0], circum_center[:,1],voronoi)
# plt.plot(voronoi[:,0], voronoi[:,1], '.')
# plt.savefig("voronoi")
# plt.show()





# # Triangle 0 is the only neighbor of triangle 1, and it’s opposite to vertex 1 of triangle 1:
# print(tri.neighbors[1]) # 第一个三角面周围有几个邻居三角形，这里只有 1 个
# print(points[tri.simplices[1,0]]) # 第 1 个三角面的 X 坐标
# print(points[tri.simplices[1,1]]) # 第 1 个三角面的 Y 坐标
# print(points[tri.simplices[1,2]]) # 第 1 个三角面的 Z 坐标
#
# # We can find out which triangle points are in:
# p = np.array([(0.1, 0.2), (1.5, 0.5)]) # 判断两个点是都在三角网内部
# print(tri.find_simplex(p))
#
# # We can also compute barycentric(重心) coordinates in triangle 1 for these points:
# b = tri.transform[1,:2].dot(p - tri.transform[1,2])
# print(tri)
# print(np.c_[b, 1 - b.sum(axis=1)])



