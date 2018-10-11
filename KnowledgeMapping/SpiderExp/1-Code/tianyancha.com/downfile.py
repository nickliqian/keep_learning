#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import time


headers = {
    'host': "dataservice.tianyancha.com",
    'connection': "keep-alive",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache",
    }


# with open("./href.list", "r") as f:
#     content = f.readlines()


content = ['企业数据服务—天眼查(W20081386501534117036011).xlsx', '企业数据服务—天眼查(W20081463431534207716774).xlsx', '企业数据服务—天眼查(W20081597661534285294438).xlsx', '企业数据服务—天眼查(W20081597661534286692800).xlsx', '企业数据服务—天眼查(W20081618751534348814200).xlsx', '企业数据服务—天眼查(W20081618751534349190424).xlsx', '企业数据服务—天眼查(W20082163431534784542753).xlsx', '企业数据服务—天眼查(W20082163431534784650831).xlsx', '企业数据服务—天眼查(W20082197661534783826278).xlsx', '企业数据服务—天眼查(W20082197661534784038035).xlsx', '企业数据服务—天眼查(W20082197661534784091927).xlsx', '企业数据服务—天眼查(W20082197661534784187504).xlsx', '企业数据服务—天眼查(W20082282251534900192746).xlsx', '企业数据服务—天眼查(W20082386501534985505090).xlsx', '企业数据服务—天眼查(W20082386501534993135604).xlsx', '企业数据服务—天眼查(W20082563431535160825466).xlsx', '企业数据服务—天眼查(W20082986501535504787061).xlsx', '企业数据服务—天眼查(W20082997661535472058849).xlsx', '企业数据服务—天眼查(W20090486501536022027903).xlsx', '企业数据服务—天眼查(W20090518751536077326791).xlsx', '企业数据服务—天眼查(W20090586501536077119063).xlsx', '企业数据服务—天眼查(W20090718751536249801882).xlsx', '企业数据服务—天眼查(W20090818751536336365603).xlsx', '企业数据服务—天眼查(W20090997661536422712838).xlsx']

for i, c in enumerate(content):
    if (i >= 0) and (i <= 10000000):
        url = "http://dataservice.tianyancha.com/excel/" + c.strip()
        print(">>> {} {}".format(i, url))
        response = requests.get(url=url, headers=headers, timeout=15)
        name = url.split("/")[-1]
        with open(name, "wb") as f:
            f.write(response.content)
        time.sleep(3)
