import requests
from lxml import etree
import re
from constant import all_cities, all_city_code, all_city_code_url
import time
import json


def get_city_url():
    url = "http://db.house.qq.com/index.php?mod=search&city=sz#LXNob3d0eXBlXzEtcGFnZV8xLXVuaXRfMS1hbGxfLUNBMV8="
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }

    response = requests.get(url=url, headers=headers)
    html = etree.HTML(response.text)
    citys = html.xpath("//div[@id='scrollBox']/div[@class='scrollContent']/dl/dd/a")

    items = []
    for city in citys:
        item = {}
        item["city_name"] = city.xpath("./text()")[0]
        item["city_url"] = city.xpath("./@href")[0]
        items.append(item)
    print(items)


def get_city_code():
    items = []

    for city in all_cities:
        item = {}
        url = city["city_url"]
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        }
        response = requests.get(url=url, headers=headers)

        html = etree.HTML(response.text)
        data = html.xpath("//dd/ul[@id='search_condition_region1']/li[1]/a/@onclick")[0]
        all_id_string = re.findall(r"\s'(.*?)'\);", data)[0]
        city_code = all_id_string.split(":")[0]
        item['city_name'] = city['city_name']
        item['city_code'] = city_code
        items.append(item)
        print(item)
        time.sleep(5)
    print()
    print(items)


def combine_city_code_url():
    items = []

    city_dict = {}
    for city in all_cities:
        city_dict[city["city_name"]] = city["city_url"]

    for city_code in all_city_code:
        item = city_code
        item["city_url"] = city_dict[city_code["city_name"]]
        print(item)
        items.append(item)
    print(items)


def get_code(city_dict):

    url = city_dict["city_url"]

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    }

    response = requests.get(url=url, headers=headers)

    html = etree.HTML(response.text)

    areas = html.xpath("//dl[@id='search_condition_container_region']/dd/ul[@id='search_condition_region1']/li/a")

    # print("area_code, area_name---------------------------------")
    area_dict = {}
    for area in areas:
        area_id = area.xpath("./@onclick")[0]
        all_id_string = re.findall(r"\s'(.*?)'\);", area_id)[0]
        area_code = all_id_string.split(":")[1]
        area_name = area.xpath("./text()")[0]
        # print(area_code, area_name)
        area_dict[area_code] = area_name

    streets_xpath = html.xpath("//dl[@id='search_condition_container_region']/dd/ul[contains(@id,'search_condition_region_business')]")

    # print("area_code, street_code, street_name------------------")
    street_items = []
    for streets_ul in streets_xpath:
        streets = streets_ul.xpath("./li/a")
        for street in streets:
            try:
                street_id = street.xpath("./@onclick")[0]
                all_id_string = re.findall(r"\s'(.*?)'\);", street_id)[0]
                street_code = all_id_string.split(":")[2]
                area_code = all_id_string.split(":")[1]
                street_name = street.xpath("./text()")[0]
                # print(area_code, street_code, street_name)
                item = {}
                item['street_code'] = street_code
                item['street_name'] = street_name
                item['area_code'] = area_code
                item['area_name'] = area_dict[area_code]
                item['city_code'] = city_dict["city_code"]
                item['city_name'] = city_dict["city_name"]

                street_items.append(item)
            except Exception:
                print(city_dict["city_name"], area_code, street_code, street_name)
    # print(street_items)

    with open("./all_code.txt", "a+") as f:
        content = json.dumps(street_items, ensure_ascii=False)
        f.write(content)
        f.write("\n")
    time.sleep(3)


def get_all_code():

    for city_dict in all_city_code_url:
        get_code(city_dict)


# d = {'city_code': '4', 'city_name': '深圳', 'city_url': 'http://db.house.qq.com/index.php?mod=search&city=sz'}
# get_code(d)

get_all_code()