#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json


sess = requests.session()

url = "https://passport.bilibili.com/login"

querystring = {"gourl": "https://space.bilibili.com"}

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'host': "passport.bilibili.com",
    'pragma': "no-cache",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

sess.request("GET", url, headers=headers, params=querystring)


url = "https://passport.bilibili.com/web/captcha/combine"

querystring = {"plat":"2"}

headers = {
    'accept': "application/json, text/plain, */*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'host': "passport.bilibili.com",
    'pragma': "no-cache",
    'referer': "https://passport.bilibili.com/login?gourl=https://space.bilibili.com",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

response = sess.request("GET", url, headers=headers, params=querystring)

chall_json = json.loads(response.text)["data"]["result"]
gt = chall_json["gt"]
challenge = chall_json["challenge"]
key = chall_json["key"]


url = "https://api.geetest.com/get.php"

querystring = {"gt": gt,
               "challenge": challenge,
               "width": "100%",
               "product": "float",
               "offline": "false",
               "protocol": "https://",
               "path": "/static/js/geetest.6.0.9.js",
               "type": "slide",
               "voice": "/static/js/voice.1.1.5.js",
               "beeline": "/static/js/beeline.1.0.1.js",
               "pencil": "/static/js/pencil.1.0.1.js",
               "callback": "callback"
               }

headers = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'host': "api.geetest.com",
    'pragma': "no-cache",
    'referer': "https://passport.bilibili.com/login?gourl=https://space.bilibili.com",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

response = sess.request("GET", url, headers=headers, params=querystring)

print(response.text)

domain = "https://static.geetest.com/"
img_data = json.loads(response.text.replace("callback(", "").replace(")", ""))


def save_img(xx):
    hh = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }
    u = "{}{}".format(domain, xx)
    print(u)
    r = sess.get(url=u, headers=hh)
    with open("{}.jpg".format(xx.replace("/", "_")), "wb") as f:
        f.write(r.content)


slice = img_data["slice"]
bg = img_data["bg"]
fullbg = img_data["fullbg"]

save_img(slice)
save_img(bg)
save_img(fullbg)

