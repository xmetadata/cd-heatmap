# -*- coding: UTF-8 -*-
import json
import time
import urllib
from difflib import SequenceMatcher

import pymongo
import requests
from bson import ObjectId
from bson.json_util import dumps, loads
from shapely.geometry import Point, Polygon

GEOCODING_URL = 'http://api.map.baidu.com/geocoding/v3/?address=%s&output=json&ak=j1rB54xkUHAoEp41Z6FwXwyXVVgASoDE'
SEARCH_URL = 'http://api.map.baidu.com/place/v2/search?region=%E8%A5%BF%E5%AE%89%E5%B8%82&city_limit=true&output=json&ak=j1rB54xkUHAoEp41Z6FwXwyXVVgASoDE&query='
DATASETFREE = 'http://127.0.0.1:5050/apiserver/v1.0/datasetfree/'
MATCH_RATE = 0.7
DEFAULT_HEADERS = ["标题", "地址", "经度", "纬度", "板块", "数值"]
DEFAULT_BLOCK_HEADERS = ["板块", "数值"]


def init_mongo():
    client = pymongo.MongoClient('mongodb://root:Aa888888@47.103.36.82:27017')
    return client['heatmap']


def fetch_collection(col_name, pipeline):
    db = init_mongo()
    result = db[col_name].aggregate(pipeline)
    return json.loads(dumps(result))


def distinct_collection(col_name, field):
    db = init_mongo()
    return db[col_name].distinct(field)


def insert_collection(col_name, data):
    db = init_mongo()
    if col_name in db.list_collection_names():
        return
    result = db[col_name].insert_many(data)
    return result.inserted_ids


def delete_collection(col_name):
    db = init_mongo()
    if col_name in db.list_collection_names():
        db[col_name].drop()


def analysis_dataset_block(col_name, data, blocks, headers):
    # 写入数据库
    insert_collection(col_name, data)
    # 导航数据
    navigate = []
    for header in (list(set(headers).difference(set(DEFAULT_BLOCK_HEADERS)))):
        navigate.append({
            'label': header,
            'options': distinct_collection(col_name, header)
        })
    # 回调更新状态
    jsondata = {
        'complete': True,
        'navigate': json.dumps(navigate),
        'headers': json.dumps(list(set(headers).union(set(DEFAULT_BLOCK_HEADERS)))),
    }
    result = requests.put(DATASETFREE + col_name[1:], json=jsondata)


def analysis_dataset(col_name, data, blocks, headers):
    # 编排板块
    polygons = []
    for block in blocks:
        if not block.coordinates:
            continue
        polygon = {
            'title': block.title,
            'polygon': Polygon([(item['lng'], item['lat']) for item in json.loads(block.coordinates)])
        }
        polygons.append(polygon)
    # 编排数据
    dataset = []
    for item in data:
        # 获取经纬度
        if item.get('经度', '') and item.get('纬度', ''):
            pass
        else:
            location = None
            address = item.get('地址', '')
            if address:
                # 根据地址找位置
                location = geocoding(address)
            else:
                # 根据名称找位置
                title = item.get('标题', '')
                if title:
                    result = geosearch(title)
                    if result:
                        item['地址'], location = result['address'], result['location']
                else:
                    pass
            if location:
                item.update({
                    '经度': location['lng'],
                    '纬度': location['lat']
                })
        # 获取归属板块
        if item.get('板块', ''):
            pass
        else:
            if item.get('经度', '') and item.get('纬度', ''):
                item['板块'] = find_polygon(
                    Point(item['经度'], item['纬度']), polygons)
            else:
                pass
        dataset.append(item)
    # 写入数据库
    insert_collection(col_name, data)
    # 导航数据
    navigate = []
    for header in (list(set(headers).difference(set(DEFAULT_HEADERS)))):
        navigate.append({
            'label': header,
            'options': distinct_collection(col_name, header)
        })
    # 回调更新状态
    jsondata = {
        'complete': True,
        'navigate': json.dumps(navigate),
        'headers': json.dumps(list(set(headers).union(set(DEFAULT_HEADERS))))
    }
    result = requests.put(DATASETFREE + col_name[1:], json=jsondata)


def geocoding(address):
    # 50QPS
    result = requests.get(GEOCODING_URL % address)
    if result.status_code == requests.codes.OK:
        jsondata = result.json()
        if jsondata['status']:
            print('geocoding', jsondata)
            return None
        return jsondata['result']['location']


def geosearch(title):
    # 2QPS
    time.sleep(0.5)
    result = requests.get(SEARCH_URL + title)
    if result.status_code == requests.codes.OK:
        jsondata = result.json()
        if jsondata['status']:
            print('geosearch', jsondata)
            return None
        for item in jsondata['results']:
            if SequenceMatcher(None, item['name'], title).quick_ratio() > MATCH_RATE:
                return item


def find_coordinates(description):
    coordinates = []
    for item in description.split('\n'):
        item = item.strip()
        coordinate = {
            'lng': float(item.split(',')[0]),
            'lat': float(item.split(',')[1]),
        }
        coordinates.append(coordinate)
    return coordinates


def find_polygon(point, polygons):
    for polygon in polygons:
        if polygon['polygon'].contains(point):
            return polygon['title']


def find_centroid(coordinates):
    polygon = Polygon([(item['lng'], item['lat']) for item in coordinates])
    centroid = polygon.centroid
    return {
        'lng': centroid.x,
        'lat': centroid.y,
    }


def calculate_area(coordinates):
    polygon = Polygon([(item['lng'], item['lat']) for item in coordinates])
    return round(polygon.area * 9000, 4)
