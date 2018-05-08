import json
import requests
import time
from lxml import etree
import re

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                         " (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}


def crawl_xiaoqu(street_url, origin):
    print("\nCrawl >>> " + street_url)
    response = requests.get(url=street_url, headers=headers)
    print(response)
    print(response.status_code)
    html = etree.HTML(response.text)

    count = html.xpath("/html/body/div[@class='content']/div[@class='leftContent']/div[@class='resultDes clear']/h2[@class='total fl']/span/text()")[0]

    print(">>> 本街道共有小区{}个".format(count))

    if int(count) == 0:
        return None

    results = html.xpath("/html/body/div[@class='content']/div[@class='leftContent']/ul[@class='listContent']"
                       "/li[@class='clear xiaoquListItem']")

    print("---------------本页的小区为---------------")
    for result in results:
        # 小区名称
        builing_name = result.xpath("./div[@class='info']/div[@class='title']/a/text()")[0]
        # 小区详情页面链接
        builing_href = result.xpath("./div[@class='info']/div[@class='title']/a/@href")[0]
        # 小区信息
        houseInfo = result.xpath("./div[@class='info']/div[@class='houseInfo']/a")
        house_type_count = None
        if len(houseInfo) == 3:
            house_type_count = houseInfo[0].xpath("./text()")[0]
            house_type_count = re.findall(r"共(\d+)个", house_type_count)[0]

        # 30天内成交套数
        house_buy = houseInfo[-2].xpath("./text()")[0]
        house_buy = re.findall(r"成交(\d+)套", house_buy)[0]

        # 正在出租的数量
        house_rent = houseInfo[-1].xpath("./text()")[0]
        house_rent = re.findall(r"(\d+)套正在出租", house_rent)[0]

        houseFeature = result.xpath("./div[@class='info']/div[@class='positionInfo']/a")
        house_district = houseFeature[0].xpath("./text()")[0]
        house_bizcircle = houseFeature[1].xpath("./text()")[0]

        house_type = result.xpath("./div[@class='info']/div[@class='positionInfo']/text()")

        house_type_string = house_type[3].replace("\xa0", "").replace("\n", "").replace(" ", "").strip("/")
        year = house_type_string.split("/")[-1]
        year = re.findall(r"(.*?)年建成", year)[0]

        price_data = time.strftime("%Y%m%d")

        # 价格
        price = result.xpath(".//div[@class='totalPrice']/span/text()")[0].strip()
        price_desc = result.xpath(".//div[@class='priceDesc']/text()")[0].strip()

        print(price_data, builing_name, builing_href, house_type_count, house_buy, house_rent, house_district, house_bizcircle, year, house_type_string, price, price_desc)

    if int(count) > 30:
        try:
            j_next = html.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]
            cur_page = int(eval(j_next)["curPage"])
            total_page = int(eval(j_next)["totalPage"])
            print(">>> 本页是第{}页，共有{}页".format(cur_page, total_page))
            if cur_page == total_page:
                print(">>> 本街道已经采集完成")
                return None
            else:
                pg = "pg" + str(cur_page + 1) + "/"
                time.sleep(5)
                return origin + pg
        except Exception as e:
            raise e
    else:
        print(">>> 无下一页")


if __name__ == '__main__':
    url = "https://gz.lianjia.com/xiaoqu/conghua1/"
    origin = url
    while True:
        if url:
            url = crawl_xiaoqu(url, origin)
        else:
            break
