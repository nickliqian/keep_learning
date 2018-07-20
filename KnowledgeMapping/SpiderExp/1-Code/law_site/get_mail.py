#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
import time
from lxml import etree


def check_mail(mail):
    url = "http://www.bccto.me/getmail"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

    while True:
        var_a = str(time.time()).replace(".", "")[:-7]
        var_b = str(time.time()).replace(".", "")[:-4]
        data = {
            "mail": str(mail),
            "time": var_a,
            "_": var_b,
        }
        response = requests.post(url=url, headers=headers, data=data)
        print(response.text)
        r_data = json.loads(response.text)

        result = r_data["mail"]
        if result:
            print("Get mail -> {}".format(result))
            return result[0][4]
        else:
            print("No mail")
        time.sleep(2)


def req_mail_href(mail_href):
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
    response = requests.get(url=mail_href, headers=headers)
    # print(response.text)
    html = etree.HTML(response.text)
    active_href = html.xpath("//a/@href")[0]
    print(active_href)
    return active_href


def req_active_href(active_href):
    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }
    response = requests.get(url=active_href, headers=headers)
    print(response.text)
    # html = etree.HTML(response.text)
    # active_href = html.xpath("//a/@href")[0]
    # print(active_href)
    # return active_href


def main():
    # 初始化参数
    use_mail = "aciyz2pa@dawin.com"
    mail_string = use_mail.replace("@", "(a)").replace(".", "-_-")
    # 到邮件查收消息
    msg = check_mail(use_mail)
    # 拼接邮件地址
    href = "http://mail.bccto.me/win/{}/{}".format(mail_string, msg)
    print(href)
    # 请求邮件，抽取激活地址
    active_href = req_mail_href(href)
    # 请求激活地址
    req_active_href(active_href)


if __name__ == '__main__':
    main()