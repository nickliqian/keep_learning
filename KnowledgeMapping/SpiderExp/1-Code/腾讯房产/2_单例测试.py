import requests
from lxml import etree
import re


def to_chinese(string):
    return string.encode('utf-8').decode('unicode_escape')


url = "http://db.house.qq.com/index.php?mod=search&act=newsearch&city=sz&showtype=1&page_no=2&mod=search&city=sz"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}

response = requests.get(url=url, headers=headers)

# 抽取文本
results = re.findall(r'var\ssearch_result\s=\s"(.*?);var\ssearch_result_list_num\s=\s(.*?);', response.text)
result = results[0]

# 本分类总数
count = int(result[1])
# html源码转换
text = result[0].replace(r'\"', '"').replace(r"\/", "/")

# lxml解析
html = etree.HTML(text)
buildings = html.xpath("//div[@class='textList fl']")


for building in buildings:

    # 楼盘名称
    build_name = to_chinese(building.xpath(".//h2/a/text()")[0]).strip()

    # 楼盘链接
    build_name_href = to_chinese(building.xpath(".//h2/a/@href")[0]).strip()

    # 楼盘状态
    build_status = to_chinese(building.xpath(".//li[@class='title']/span/text()")[0]).strip()

    # 楼盘户型
    build_house_type_xpath = building.xpath(".//li[@class='h_type']/a/text()")
    if build_house_type_xpath:
        build_house_type = to_chinese(",".join(build_house_type_xpath)).strip()
    else:
        build_house_type = "暂无资料"

    # 楼盘地址
    build_address = to_chinese(building.xpath(".//li[@class='address']/@title")[0]).strip()
    if not build_address:
        build_address = to_chinese(building.xpath(".//li[@class='address']/a/text()")[0]).strip()

    # 楼盘标签
    build_tags_xpath = building.xpath(".//li[@class='tags']/a/text()")
    if build_tags_xpath:
        build_tags = to_chinese(",".join(build_tags_xpath)).strip()
    else:
        build_tags = "暂无标签"

    # 楼盘价格
    build_price_type = to_chinese(building.xpath(".//li[@class='title']/p[@class='fr']/text()")[0]).strip()
    build_price_price = to_chinese(building.xpath(".//li[@class='title']/p[@class='fr']/a/text()")[0]).strip()
    build_price_unit = to_chinese(building.xpath(".//li[@class='title']/p[@class='fr']/text()")[1]).strip()

    print("{:<15s}{:<30s}{:<10s}{:<30s}{:<30s}{:<15s}{:<15s}{:<15s}{:<15s}"
          .format(build_name, build_name_href, build_status,
                  build_house_type, build_address, build_tags,
                  build_price_type, build_price_price, build_price_unit
                  ))
