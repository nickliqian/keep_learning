import requests
from lxml import etree
import json
import time


def get_json_sample():
    url = "http://m.sofang.com/sz/saleesb/area?f=h5&page=1"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }

    response = requests.get(url=url, headers=headers)

    data_dict = json.loads(response.text)

    print(data_dict["businessAreas"])
    print(data_dict["cityAreas"])


def get_city_detail_url(city):
    target_url = city["city_url"] + "/saleesb/area"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
    }

    response = requests.get(url=target_url, headers=headers, timeout=6)

    html = etree.HTML(response.text)

    areas = html.xpath("//div[@class='area_box']/ul[contains(@class,'box_area')]/li/text()")
    area_uls = html.xpath("//div[@class='area_box1 ']/ul[contains(@class,'box_area1')]")

    count = 0
    items = []
    for i in range(1, len(area_uls)):
        streets = area_uls[i].xpath("./li/a")
        for j in range(1, len(streets)):
            item = dict()
            item['city_name'] = city["city_name"]
            item['area_name'] = areas[i-1]
            item['street_name'] = streets[j].xpath("./text()")[0]
            item['street_url'] = "http://m.sofang.com" + streets[j].xpath("./@href")[0]
            items.append(item)
            count += 1
    print("a", count)
    return items


def all_city_url():
    with open("./city_map.json", "r") as f:
        cities = json.load(f)
    return cities


if __name__ == '__main__':
    info_list = []

    city_list = all_city_url()
    for city_dict in city_list:
        print("------------->{}".format(city_dict))
        r = get_city_detail_url(city_dict)
        print("b", len(r))
        info_list.append(r)
        time.sleep(5)

    data = json.dumps(info_list, ensure_ascii=False)
    with open("./streets.json", "w") as f:
        f.write(data)