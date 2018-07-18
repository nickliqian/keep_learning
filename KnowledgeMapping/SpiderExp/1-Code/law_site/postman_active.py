#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

url = "http://mail.bccto.me/win/aciyz2pa%28a%29dawin-_-com/XKcYhWhgh1ACIHX6PR4cG6.eml"

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache",
    'host': "mail.bccto.me",
    'pragma': "no-cache",
    'proxy-connection': "keep-alive",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

response = requests.request("GET", url, headers=headers)

print(response.text)