# -*- coding:utf-8 -*-
from typing import List

from scripts.entry import LocationEntry

# 0922更新：可一次查询多个行政区。另外，对未知地点的搜索词，增加了城市比对功能，提升了检查效率，减少对key的消耗。
# 使用方式：已知地址，按regions=['027','010','028']格式输入regions参数（注意必须都是英文字符），对于未知地址，输入regions=[]即可


# 注意：V3与V5搜索的结果不完全相同！V5是高德搜索2.0，比V3能搜到更多结果！

# 优化内容：1.增加百度地图自动定位功能：在结果csv文件夹中，针对每条结果数据，按“crtl”并点击该条的网址，即可在高德或百度地图中定位到该地点（前一条为高德，后一条为百度）。2.增加了csv文档自动清空功能：每次运行前，会清空与本次储存文件同名的csv文件。3.增添了错误提示功能。4.修复了原有的v3搜索出错的地方，现在应该无论v3还是v5（搜索服务2.0）搜索都不会出错了。原来的限制了城市但还是跑全国的bug应该也没了，如果还有问题麻烦私戳我。

# 首次运行前，请在下方“终端”界面，输入'pip install requests',之后运行无需再次输入

# 输入参数

gaode_key = '84050bc604e0509ee16c13c62e4436c9'  # 从高德地图开放平台获取web服务key值，替换''内的内容

# regions = [
#     '350000']  # 已知地点的格式：['027','010','028']，对于未知地址，按regions=[]输入。编号从“高德地图行政区编号.csv”文件中查找，可输入citycode，adcode。填写尽量准确的信息
#
# keywords1 = '资溪面包'  # 与type1至少选填其中一项，为了准确考虑建议填写，首要关键词，尽量准确，选择个数较少的地址作为首要关键词，多个关键字用“|”分割
#
# type1 = ''  # 与keywords1至少选填其中一项，从“高德地图poi分类编号.csv”文件中查找，填写尽量准确的信息，可以传入多个编号，相互之间用“|”分隔，
#
# keywords2 = '体验馆'  # 约束条件，在首要关键词搜索结果中查找附近有第二个关键词的地址，多个关键字用“|”分割,与type2至少选填其中一项
#
# radius = '30'  # 搜索范围，单位为米，即搜索前一个关键词附近多少米范围内的第二个关键词，取值范围:0-50000，大于50000时按默认值
#
# type2 = ''  # 与keywords2至少选填其中一项，从“高德地图poi分类编号.csv”文件中查找，填写尽量准确的信息，可以传入多个编号，相互之间用“|”分隔，
#
# filename = '检索结果.csv'  # 结果储存在改文件内，文件名可修改（勿动后缀）
#
# 以下勿动

bdkey = 'YplBscmFRhGmn7ooB1FhKAnG8VR297GC'  # 百度ak

import os
import requests


# 关键字爬取
def get_poi_text(key, region, keywords, type, page):
    if type == None:
        type = ''
    # 用v3就在下面第1条url加#，用v5就在下面第2条url加#，默认v5（较准确，但v3额度比较大）
    # url = 'https://restapi.amap.com/v5/place/text?page_size=25&page_num=' +str(page)+ '&key=' + key+'&keywords='+keywords+'&types='+type+'&region='+region+'&city_limit=True'
    url = 'https://restapi.amap.com/v3/place/text?key=' + key + '&keywords=' + keywords + '&types=' + type + '&city=' + region + '&city_limit=True&offset=25&page=' + str(
        page)

    get_json = requests.get(url=url).json()
    poi_infos = []
    for item in get_json['pois']:
        try:
            poi_info = [item['name'], item['location'], item['id'],
                        item['pname'] + item['cityname'] + item['adname'] + item['address']]
        except BaseException:
            poi_info = [item['name'], item['location'], item['id'], item['pname'] + item['cityname'] + item['adname']]
        poi_infos.append(poi_info)
    return poi_infos


def get_near_poi(key, location, radius, keyword, type):
    if type == None:
        type = ''
    # 用v3就在下面第1条url加#，用v5就在下面第2条url加#，默认v5（较准确，但v3额度比较大）
    # url ='https://restapi.amap.com/v5/place/around?key='+key+'&keywords='+keyword+'&types='+type+'&location='+location+'&radius='+radius+'&page_size=25&sortrule=distance'
    url = 'https://restapi.amap.com/v3/place/around?key=' + key + '&keywords=' + keyword + '&types=' + type + '&location=' + location + '&radius=' + radius + '&offset=25&sortrule=distance'

    get_json = requests.get(url=url).json()
    count = get_json['count']

    poi_infos = []
    if int(count) > 0:
        poi_info = [item['name'] for item in get_json['pois']]
        poi_infos.extend(poi_info)

    return count, poi_infos


def get_bdlacation(key, location):
    # 勿动
    url = 'https://api.map.baidu.com/geoconv/v1/?coords=' + location + '&from=3&to=5&ak=' + key

    get_json = requests.get(url=url).json()['result'][0]

    poi_info = [get_json['y'], get_json['x']]

    return poi_info


# 获取poi分布城市
def get_poi_city(key, keywords, type):
    if type == None:
        type = ''
    url = 'https://restapi.amap.com/v3/place/text?keywords=' + keywords + '&offset=20&page=1&key=' + key + '&extensions=all&types=' + type
    get_json = requests.get(url=url).json()
    cities = []
    accodes = []
    for item in get_json['suggestion']['cities']:
        accodes.append(item['citycode'])
    return accodes


def query(regions: List[str], keywords1, type1, keywords2, type2, radius ):

        # 获取合适地点列表
    if regions is None or regions == []:
        keyword1codes = get_poi_city(gaode_key, keywords1, type1)
        keyword2codes = get_poi_city(gaode_key, keywords2, type2)
        for c in keyword1codes:
            if c in keyword2codes:
                regions.append(c)
        if regions == []:
            print('没有包含关键词1和关键词2的城市，请检查后再查询')
            os._exit(0)
        else:
            pass
    results = []
    for region in regions:
        try:
            page = 1
            poi1_number = 25
            while poi1_number > 24:
                try:
                    data1 = get_poi_text(gaode_key, region, keywords1, type1, page)
                    poi1_number = len(data1)
                    info = '对第' + str(page) + '次搜索关键词“' + keywords1 + '”返回的' + str(
                        poi1_number) + '个结果进行周边查找'
                    print(info)
                    page += 1

                    for poi in data1:
                        data2 = get_near_poi(gaode_key, poi[1], radius, keywords2, type2)
                        if int(data2[0]) > 0:
                            amap_link = 'https://www.amap.com/place/' + str(poi[2])
                            location = get_bdlacation(bdkey, poi[1])
                            baidu_link = 'https://map.baidu.com/?latlng=' + str(location[0]) + ',' + str(location[1])
                            print(data2)
                            entry = LocationEntry(
                                name1=poi[0],
                                lat_long=poi[1],
                                amap_id=poi[2],
                                address=poi[3],
                                keyword2_count=data2[0],
                                name2=data2[1],
                                amap_link=amap_link,
                                baidu_link=baidu_link
                            )
                            results.append(entry)

                except BaseException:
                    print('查询出错，请检查1.高德key是否超出当日限额，2.url地址是否配置正确')
                    break
        except BaseException:
            print('查询出错，请检查1.高德key是否超出当日限额，2.url地址是否配置正确')
            break
        return results



