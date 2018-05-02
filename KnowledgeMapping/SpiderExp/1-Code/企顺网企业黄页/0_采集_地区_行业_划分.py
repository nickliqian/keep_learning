import redis
import requests
from lxml import etree
import json


def get_area_code():
    url = "http://www.11467.com/dir.html"

    r = requests.get(url=url)

    html = etree.HTML(r.text)
    s = html.xpath("//dd/a")

    items = []
    for i in s:
        item = {}
        name = i.xpath("./@title")[0].replace("黄页", "")
        href = i.xpath("./@href")[0].strip("/").split("/")[-1]
        item["name"] = name
        item["href"] = href
        print(item)
        items.append(item)

    with open("./a地域列表.json", "w") as f:
        json.dump(items, f, ensure_ascii=False)


def get_industry_code():
    # //ul[@class='listtxt']/li/dl//a
    url = "http://www.11467.com/shenzhen/"

    r = requests.get(url=url)

    html = etree.HTML(r.text)
    s = html.xpath("//ul[@class='listtxt']/li/dl//a")

    items = []
    for i in s:
        item = {}
        name = i.xpath("./text()")[0].replace("黄页", "").replace("深圳", "")
        href = i.xpath("./@href")[0].split("shenzhen")[-1]
        item["name"] = name
        item["href"] = href
        print(item)
        items.append(item)

    with open("./b行业列表.json", "w") as f:
        json.dump(items, f, ensure_ascii=False)


def get_area_industry_dict():
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    redis_conn = redis.Redis(connection_pool=redis_pool)

    domain = "http://www.11467.com"

    with open("./a地域列表.json", "r") as f:
        area_dicts = json.load(f)
    with open("./b行业列表.json", "r") as f:
        industry_dicts = json.load(f)

    for area in area_dicts:
        for industry in industry_dicts:
            content = {}
            url = "{}/{}{}".format(domain, area["href"], industry["href"])
            content["url"] = url
            content["area"] = area["name"]
            content["industry"] = industry["name"]
            print(content)
            redis_conn.sadd("qishun_list", content)


if __name__ == '__main__':
    get_area_industry_dict()