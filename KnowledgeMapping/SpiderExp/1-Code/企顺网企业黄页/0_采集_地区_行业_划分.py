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


def get_more_industry_code():
    url = "http://www.11467.com/shenzhen/"
    r = requests.get(url=url)

    html = etree.HTML(r.text)
    lis_1 = html.xpath("/html/body/div[@id='main']/div[@id='il']/div[@class='box sidesubcat t5'][1]/div[@class='boxcontent']/dl[@class='listtxt']/dd/a")

    lis_2 = html.xpath("/html/body/div[@id='main']/div[@id='il']/div[@class='box sidesubcat t5'][2]/div[@class='boxcontent']/dl[@class='listtxt']/dd/a")

    items = []
    for l in lis_1:
        item = dict()
        item["name"] = l.xpath("./text()")[0].strip("深圳").strip("黄页")
        item["href"] = l.xpath("./@href")[0].split("shenzhen")[-1]
        print(item)
        items.append(item)
    print()
    for l in lis_2:
        item = dict()
        item["name"] = l.xpath("./text()")[0].strip("深圳").strip("公司")
        item["href"] = l.xpath("./@href")[0].split("shenzhen")[-1]
        print(item)
        items.append(item)

    print(items)
    with open("./c更多行业列表.json", "w") as f:
        json.dump(items, f, ensure_ascii=False)


def get_area_more_industry_dict():
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    redis_conn = redis.Redis(connection_pool=redis_pool)

    domain = "http://www.11467.com"

    with open("./a地域列表.json", "r") as f:
        area_dicts = json.load(f)
    with open("./c更多行业列表.json", "r") as f:
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


def combine_all_industry():
    with open("./b行业列表.json", "r") as f:
        b = json.load(f)
    with open("./c更多行业列表.json", "r") as f:
        c = json.load(f)

    all = b + c

    with open("./d所有行业列表.json", "w") as f:
        json.dump(all, f, ensure_ascii=False)


if __name__ == '__main__':
    combine_all_industry()