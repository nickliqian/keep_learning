import json
import redis
import requests
import time
from lxml import etree
import random
import urllib3


# 从redis获取代理IP
def get_proxy():
    while True:
        try:
            num_list = [i for i in range(1, 21)]
            ip_choice = random.choice(num_list)
            ip_str = "myip" + str(ip_choice)
            ip_num = r_conn.mget(ip_str)[0]
            if not ip_num:
                return None
            ip_num = ip_num.decode('utf-8')
            print("proxy: %s" % ip_num)
            return ip_num
        except Exception as e:
            print(e)
            time.sleep(1)


def req_url(url):
    while True:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            }
            r = requests.get(url=url, headers=headers, proxies={"https": get_proxy()}, timeout=8, verify=False)
            return r
        except Exception as e:
            print(type(e), e)


# 49个城市
def get_main_city_href():
    url = "https://cc.anjuke.com/community/"

    response = req_url(url)
    html = etree.HTML(response.text)

    results = html.xpath("//dl/dd/a")
    items = []
    for result in results:
        item = dict()
        item['city'] = result.xpath("./text()")[0]
        item['city_href'] = result.xpath("./@href")[0]
        items.append(item)
        # print(item)
    return items


def verify_city_community_url(city_url_list):

    items = []
    for city_url_dict in city_url_list:
        print("\n>>> {}".format(city_url_dict))

        print("命中")
        city_url = city_url_dict["city_href"]
        if city_url.endswith("/"):
            city_url += 'community/'
        else:
            city_url += '/community/'

        # 请求城市URL
        response = req_url(city_url)
        html = etree.HTML(response.text)

        # 获取城市-行政区URL
        results = html.xpath("//div[@class='items'][1]/span[@class='elems-l pp-mod']/a[position()>1]")
        if not results:
            results = html.xpath("//div[@class='items'][1]/span[@class='elems-l ']/a[position()>1]")
        print(results)

        for result in results:

            city = city_url_dict["city"]
            area = result.xpath("./text()")[0]
            area_href = result.xpath("./@href")[0]

            # 请求街道URL
            response = req_url(area_href)
            html = etree.HTML(response.text)
            side_names = html.xpath("//span[@class='elems-l pp-mod']//div[@class='sub-items']/a[position()>1]")
            if not results:
                side_names = html.xpath("//span[@class='elems-l ']//div[@class='sub-items']/a[position()>1]")
            # 获取每个街道的详细数据-dict
            print(">>> {} >>> {} >>> {}".format(city, area, area_href))
            for side_name in side_names:
                item = dict()
                item['city'] = city
                item['city_href'] = city_url
                item['area'] = area
                item['area_href'] = area_href
                item['street'] = side_name.xpath("./text()")[0].strip()
                item['street_href'] = side_name.xpath("./@href")[0]
                # print(item)
                items.append(item)
            time.sleep(3)
    return items

        # results = html.xpath("//div[@class='li-info']/h3/a")
        # items = []
        # print(len(results))
        # for result in results:
        #     item = dict()
        #     item['city'] = result.xpath("./text()")[0]
        #     item['href'] = result.xpath("./@href")[0]
        #     items.append(item)
        #     # print(item)
        #     return
        #     time.sleep(3)


def transfer_json(items):
    data = json.dumps(items, ensure_ascii=False)
    with open("./map.json", "w", encoding="utf-8") as f:
        f.write(data)


def check_json_rows(file_name):
    with open(file_name, "r") as f:
        data = json.load(f)
    print(len(data))
    print(type(data))
    print(data[0])
    print(data[-1])


if __name__ == '__main__':
    urllib3.disable_warnings()

    r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    # 生成站点地图 json
    city_map = get_main_city_href()
    street_json = verify_city_community_url(city_map)
    transfer_json(street_json)

    # 检查json文件行数
    # check_json_rows("123map.json")

