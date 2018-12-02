#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/65.0.3325.146 Safari/537.36",
}


def req_base_html():
    # 1 请求基本页面
    url = "https://www.anjuke.com/captcha-verify/"
    params = {
        "callback": "shield",
    }
    response = requests.get(url=url, params=params, headers=headers)
    print(response)
    sessionId = ""

    return sessionId


def get_umg_url(sessionId):
    # 2 获取图片的url
    url = "https://verifycode.58.com/captcha/getV3"
    params = {
        "callback": "jQuery191031627949098677566_1543724836402",
        "showType": "embed",
        "sessionId": sessionId,
        "_": "1543724836403"
    }
    response = requests.get(url=url, params=params, headers=headers)

    responseId = ""
    return responseId


def get_img(responseId):
    # 3 请求图片 大图+小图
    url = "https://verifycode.58.com/captcha/captcha_img"
    params = {
        "rid": responseId,
        "it": "_big"
    }
    response = requests.get(url=url, params=params, headers=headers)
    print(response)

    params = {
        "rid": responseId,
        "it": "_puzzle"
    }
    response = requests.get(url=url, params=params, headers=headers)
    print(response)

    big_image_file = response.content
    return big_image_file