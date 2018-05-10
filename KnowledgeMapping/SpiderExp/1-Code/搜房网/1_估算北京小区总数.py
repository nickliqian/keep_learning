import requests
import time
from lxml import etree


def get_sub_page():
    domain = "http://bj.sofang.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    r1 = requests.get(url="http://bj.sofang.com/saleesb/area/aa5", headers=headers)
    html = etree.HTML(r1.text)

    results = html.xpath("//div[@class='search_info']/dl[1]/dd[1]/a")

    items = []
    for result in results:
        item = dict()
        item["name"] = result.xpath("./text()")[0]
        item["href"] = domain + result.xpath("./@href")[0]
        if not item["name"] == "不限":
            items.append(item)
            # print(item)

    return items


def get_page_num(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    r1 = requests.get(url=url, headers=headers)
    html = etree.HTML(r1.text)

    page_num = html.xpath("//div[@class='list_l']/div[@class='page_nav']/ul/li[last()-2]/a[@class='page']/text()")[0]

    return int(page_num)


if __name__ == '__main__':

    task = get_sub_page()

    print("地区 页码数 总页码")
    num = 0
    for t in task:
        p = get_page_num(t["href"])
        num += p
        print("<{}> <{}> <{}>".format(t["name"], p, num))
        time.sleep(3)

    print("总数：{}".format(num*25))