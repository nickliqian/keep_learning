import requests
from lxml import etree
import time
from constant import pro_list


start = False
for pro in pro_list:

    area_name = pro[0]  # 北京
    number = pro[1]  # 1000
    url_location = pro[2]  # beijing

    if area_name == "广东":
        start = True

    if start:

        url = "https://gongshang.mingluji.com/{}/list".format(url_location)
        query_string = {
            "page": "0",
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
        }

        response = requests.get(url=url, params=query_string, headers=headers, timeout=15, verify=False)

        html = etree.HTML(response.text)
        results = html.xpath("//div[@class='item-list']/ol/li/div[@class='views-field views-field-title']/span[@class='field-content']/a")
        print("{} - {}个 - {}个/组 - {}组".format(area_name, number, len(results), number/len(results)))

        time.sleep(5)

