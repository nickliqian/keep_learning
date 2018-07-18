#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import time
from lxml import etree


# 登陆注册页获得cookie和csrf value
sess = requests.Session()
url = "http://openlaw.cn/register.jsp"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
}
response = sess.get(url=url, headers=headers)
print(response.cookies.items())
html = etree.HTML(response.text)
csrf_value = html.xpath("//input[@name='_csrf']/@value")[0]
print("csrf_value {}".format(csrf_value))

# 获取验证码
v = str(time.time()).replace(".", "")[:-4]
url = "http://openlaw.cn/Kaptcha.jpg?v={}".format(v)
response = sess.get(url=url, headers=headers)
with open("./p.png", "wb") as f:
    f.write(response.content)

# 输入验证码
verify_value = str(input("Input validate code:"))

# 注册
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "Referer": "http://openlaw.cn/register.jsp",
}
data = {
    "_csrf": csrf_value,
    "email": "aciyz2pa@dawin.com",
    "userName": "aciyz2pa@dawin.com",
    "nickName": "aciyz2pa",
    "password": "1qaz@WSX",
    "validateCode": verify_value,
    "agree": "forever",
}
url = "http://openlaw.cn/service/rest/us.User/collection/register"
print(data)
response = sess.request("POST", url=url, headers=headers, data=data)
print(response.text)