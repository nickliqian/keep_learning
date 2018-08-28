#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from lxml import etree

"""
验证码地址
"""

url = "http://www1.soopat.com/Home/Result"

querystring = {
    "SearchWord": "SQR:('乐视控股(北京)有限公司')",
    "PatentIndex": "10"
}

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache",
    'host': "www1.soopat.com",
    'pragma': "no-cache",
    'proxy-connection': "keep-alive",
    'referer': "http://www1.soopat.com/Home/Result?SearchWord=SQR%3A(%22%E4%B9%90%E8%A7%86%E6%8E%A7%E8%82%A1(%E5%8C%97%E4%BA%AC)%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22)",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    'postman-token': "6ecc3b3f-d2c2-dde3-1635-a15f8b567dda"
}

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)


html = etree.HTML(response.text)
ele = html.xpath("//div")
print(ele)
if ele:
    raw = etree.tounicode(ele[0], method='html')
    print(raw)
else:
    print("no tags")
