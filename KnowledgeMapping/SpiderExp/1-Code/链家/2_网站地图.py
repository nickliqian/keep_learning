import json

import requests
import time
from lxml import etree


city_list_dict = [{'name': '深圳', 'code': 'sz'}, {'name': '北京', 'code': 'bj'}, {'name': '济南', 'code': 'jn'},
                  {'name': '合肥', 'code': 'hf'}, {'name': '成都', 'code': 'cd'}, {'name': '东莞', 'code': 'dg'},
                  {'name': '南京', 'code': 'nj'}, {'name': '长沙', 'code': 'cs'}, {'name': '武汉', 'code': 'wh'},
                  {'name': '沈阳', 'code': 'sy'}, {'name': '重庆', 'code': 'cq'}, {'name': '大连', 'code': 'dl'},
                  {'name': '天津', 'code': 'tj'}, {'name': '苏州', 'code': 'su'}, {'name': '杭州', 'code': 'hz'},
                  {'name': '广州', 'code': 'gz'}, {'name': '佛山', 'code': 'fs'}, {'name': '青岛', 'code': 'qd'},
                  {'name': '烟台', 'code': 'yt'}, {'name': '厦门', 'code': 'xm'}, {'name': '上海', 'code': 'sh'}]
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                         " (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}


def test_city_have_xiaoqu():
    for city in city_list_dict:
        url = "https://{}.lianjia.com/xiaoqu/".format(city["code"])
        print(url)
        response = requests.get(url=url, headers=headers)
        html = etree.HTML(response.text)
        result = html.xpath("/html/body/div[@class='content']/div[@class='leftContent']"
                            "/div[@class='resultDes clear']/h2[@class='total fl']/text()")
        print(result)
        time.sleep(3)


def crawl_area_href(city):
    # 构造不同城市的链接
    domain = "https://{}.lianjia.com".format(city["code"])
    # 构造小区链接
    city_url = domain + "/xiaoqu/"
    # 发送请求
    response = requests.get(url=city_url, headers=headers)
    # 抓取每个街道的名称和链接
    html = etree.HTML(response.text)
    areas = html.xpath("/html/body/div[@class='m-filter']/div[@class='position']/dl[2]/dd/div/div[1]/a")
    for area in areas:
        area_name = area.xpath("./text()")[0]
        area_href = area.xpath("./@href")[0]
        city["area"] = area_name
        if area_href.startswith("/"):
            area_href = domain+area_href
        print(area_name, area_href)
        crawl_street_href(area_href, city)
    time.sleep(3)


def crawl_street_href(url, city):
    # 构造不同城市的链接
    domain = "https://{}.lianjia.com".format(city["code"])
    # 发送请求
    response = requests.get(url=url, headers=headers)
    # 抓取每个街道的名称和链接
    html = etree.HTML(response.text)
    streets = html.xpath("/html/body/div[@class='m-filter']/div[@class='position']/dl[2]/dd/div/div[2]/a")
    for street in streets:
        street_name = street.xpath("./text()")[0]
        street_href = street.xpath("./@href")[0]
        if street_href.startswith("/"):
            street_href = domain+street_href
        city["street"] = street_name
        city["href"] = street_href
        print(city)
        items.append(city)
    time.sleep(3)


if __name__ == '__main__':
    items = []
    # 采集每个街道对应的链接放入列表 [{},{}...]
    for city_dict in city_list_dict:
        crawl_area_href(city_dict)
    # 列表数据转为json字符串
    rows_data = json.dumps(items, ensure_ascii=False)
    # json字符串写入文件，持久性保存
    with open("./street_map.json", "w") as f:
        f.write(rows_data)
