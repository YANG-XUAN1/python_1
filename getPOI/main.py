#!/usr/bin/env python
# -*- coding:utf-8 -*-

from urllib.parse import quote
from urllib import request
import json
import xlwt
import csv

#TODO 替换为申请的密钥
# amap_web_key = 'ba5d4bf94af4949354ac7d380861b156'
amap_web_key='d5d621001ab70499e41f17d4645c0e49'

poi_search_url = "http://restapi.amap.com/v3/place/text"
poi_boundary_url = "https://ditu.amap.com/detail/get/detail"
#from transCoordinateSystem import gcj02_to_wgs84

#TODO cityname为需要爬取的POI所属的城市名，city_areas为城市下面的行政区，classes为多个POI分类名的集合.
# (中文名或者代码都可以，代码详见高德地图的POI分类编码表)
# cityname = '武汉'
cityname = '湖北'
citynames = ['北京','天津','上海','重庆','广东','内蒙古','广西','西藏','宁夏','新疆','香港','澳门','河北','山西','辽宁','吉林','黑龙江',
            '江苏','浙江','安徽','福建','江西','山东','河南','湖北','湖南','四川','贵州','云南','陕西','甘肃','青海','台湾']
city_areas = ['武昌区','江汉区','江岸区','硚口区','汉阳区','青山区','洪山区','东西湖区','汉南区','蔡甸区','江夏区','黄陂区','新洲区']
classes = ['图书馆']


# 根据城市名称和分类关键字获取poi数据
def getpois(cityname, keywords):
    i = 1
    poilist = []
    while True:  # 使用while循环不断分页获取数据
        result = getpoi_page(cityname, keywords, i)
        # print(result)
        result = json.loads(result)  # 将字符串转换为json
        if result['count'] == '0':
            break
        hand(poilist, result)
        i = i + 1
    return poilist


# 数据写入excel
def write_to_excel(poilist):   #, cityname, classfield
    f = open('./图书馆1.csv','w',encoding='utf-8-sig')
    csv_writer = csv.writer(f)
    csv_writer.writerow(['id','lng','lat','name','cityname','province','count'])

    for i in range(len(poilist)):
        location = poilist[i]['location']
        name = poilist[i]['name']
        # address = poilist[i]['address']
        adname = poilist[i]['cityname']
        pname = poilist[i]['pname']
        lng = str(location).split(",")[0]
        lat = str(location).split(",")[1]
        # print(lng,lat,i,name,adname)
        csv_writer.writerow([i,lng,lat,name,adname,pname,'1'])

    f.close()
    # 一个Workbook对象，这就相当于创建了一个Excel文件
    # book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    # sheet = book.add_sheet(classfield, cell_overwrite_ok=True)
    #
    # # 第一行(列标题)
    # sheet.write(0, 0, 'longitude')
    # sheet.write(0, 1, 'latitude')
    # sheet.write(0, 2, 'id')
    # sheet.write(0, 3, 'name')
    # # sheet.write(0, 4, 'address')
    # sheet.write(0, 4, 'address')
    #
    #
    # for i in range(len(poilist)):
    #     location = poilist[i]['location']
    #     name = poilist[i]['name']
    #     #address = poilist[i]['address']
    #     adname = poilist[i]['adname']
    #     lng = str(location).split(",")[0]
    #     lat = str(location).split(",")[1]
    #     '''
    #     #坐标转换
    #     result = gcj02_to_wgs84(float(lng), float(lat))
    #     lng = result[0]
    #     lat = result[1]
    #     '''
    #
    #     # 每一行写入
    #     sheet.write(i + 1, 0, lng)
    #     sheet.write(i + 1, 1, lat)
    #     sheet.write(i + 1, 2, i)
    #     sheet.write(i + 1, 3, name)
    #     #sheet.write(i + 1, 4, address)
    #     sheet.write(i + 1, 4, adname)
    #
    # # 最后，将以上操作保存到指定的Excel文件中
    # #book.save(r'' + cityname + "_" + classfield + '.xls')
    # book.save(r'./酒店.xls')

# 将返回的poi数据装入集合返回
def hand(poilist, result):
    # result = json.loads(result)  # 将字符串转换为json
    pois = result['pois']
    for i in range(len(pois)):
        poilist.append(pois[i])


# 单页获取pois
def getpoi_page(cityname, keywords, page):
    req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
        keywords) + '&city=' + quote(cityname) + '&citylimit=true' + '&offset=25' + '&page=' + str(
        page) + '&output=json'
    # print(keywords,cityname)
    # req_url = poi_search_url + "?key=" + amap_web_key + '&extensions=all&keywords=' + quote(
    #     keywords) + '&citylimit=true' + '&offset=25' + '&page=' + str(
    #     page) + '&output=json'
    data = ''
    with request.urlopen(req_url) as f:
        data = f.read()
        data = data.decode('utf-8')
    return data


#按各行政区分别获取
# for clas in classes:
#     classes_all_pois = []
#     for area in city_areas:
#         pois_area = getpois(area, clas)
#         print('当前城区：' + str(area) + ', 分类：' + str(clas) + ", 总的有" + str(len(pois_area)) + "条数据")
#         classes_all_pois.extend(pois_area)
#     print("所有城区的数据汇总，总数为：" + str(len(classes_all_pois)))
#     # print(classes_all_pois)
#     write_to_excel(classes_all_pois)
#
#     print('================分类：'  + str(clas) + "写入成功")


#直接获取整个城市的POI数据
for clas in classes:
    classes_all_pois = []
    pois_area = getpois(cityname, clas)
    classes_all_pois.extend(pois_area)
    print("数据总数为：" + str(len(classes_all_pois)))
    write_to_excel(classes_all_pois)
    print('================分类：'  + str(clas) + "写入成功")

#按各行政区分别获取
# for clas in classes:
#     classes_all_pois = []
#     for area in citynames:
#         pois_area = getpois(area, clas)
#         print('当前城区：' + str(area) + ', 分类：' + str(clas) + ", 总的有" + str(len(pois_area)) + "条数据")
#         classes_all_pois.extend(pois_area)
#     print("所有城区的数据汇总，总数为：" + str(len(classes_all_pois)))
#     # print(classes_all_pois)
#     write_to_excel(classes_all_pois)
#
#     print('================================分类：'  + str(clas) + "写入成功================================")
