import requests
from lxml import etree
import time


def req_page():
    url = "http://www.qichacha.com/g_HEN_1.html"

    f = 1
    while True:
        if f > 3:
            return 0
        try:
            response = requests.get(url=url, headers=headers)
            return response
        except Exception as e:
            f += 1
            print("异常 {}".format(e))


def parse_page(resp):
    html = etree.HTML(resp.text)
    results = html.xpath("//section[@id='searchlist']/a[@class='list-group-item clearfix']")

    for result in results:
        name = result.xpath("./span[@class='clear']/span[@class='name']/text()")[0]
        href = site + result.xpath("./@href")[0]
        print("{:<18}{:^100}".format(name, href))


if __name__ == '__main__':


    # 参数设置
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    site = "http://www.qichacha.com"
    r = req_page()
    parse_page(r)

