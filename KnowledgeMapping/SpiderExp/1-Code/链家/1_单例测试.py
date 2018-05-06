import json
import requests
import time
from lxml import etree


headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                         " (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}


def crawl_xiaoqu(street_url):
    response = requests.get(url=street_url, headers=headers)
    html = etree.HTML(response.text)

    count = html.xpath("/html/body/div[@class='content']/div[@class='leftContent']/div[@class='resultDes clear']/h2[@class='total fl']/span/text()")[0]

    print("本街道共有小区{}个".format(count))


    results = html.xpath("/html/body/div[@class='content']/div[@class='leftContent']/ul[@class='listContent']"
                       "/li[@class='clear xiaoquListItem']")

    print("\n---------------本页的小区为---------------")
    for result in results:
        # 小区名称
        name = result.xpath("./div[@class='info']/div[@class='title']/a/text()")[0]
        # 小区详情页面链接
        href = result.xpath("./div[@class='info']/div[@class='title']/a/@href")[0]
        # 小区信息
        houseInfo = result.xpath("./div[@class='info']/div[@class='houseInfo']/a")
        house_type_count = None
        if len(houseInfo) == 3:
            house_type_count = houseInfo[0].xpath("./text()")[0]
        house_buy = houseInfo[-2].xpath("./text()")[0]
        house_rent = houseInfo[-1].xpath("./text()")[0]

        print(name, href, house_type_count, house_buy, house_rent)

    try:
        j_next = html.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]
        j_next = eval(j_next)
        if j_next["curPage"] == j_next["totalPage"]:
            print("本街道已经采集完成")
        else:
            pg = "pg" + str(int(j_next["curPage"] + 1)) + "/"
            crawl_xiaoqu(street_url + pg)
    except Exception as e:
        raise e


if __name__ == '__main__':
    url = "https://bj.lianjia.com/xiaoqu/chaoyangmennei1/"
    crawl_xiaoqu(url)