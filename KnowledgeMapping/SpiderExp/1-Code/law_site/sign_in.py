#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from lxml import etree


# 获取csrf参数
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
}
login_form_url = "http://openlaw.cn/login.jsp"
sess = requests.Session()
response = sess.request("GET", url=login_form_url, headers=headers)
print(response.cookies.items())
html = etree.HTML(response.text)
csrf_value = html.xpath("//input[@name='_csrf']/@value")[0]
print("csrf_value {}".format(csrf_value))


# 登陆
pwd = "FjOUpfGaybqaFkeZH7YFqOhhQPOprUJCoKQ/v7hbfe6AplyztqTV95oa9zwkz2rHoXL4aUXL/678GOa8bidaIaAMCnYAs39/YkVIQKcvJYZC3u" \
      "IP3Q4bhnhi8SnVm6S6R2n4QnDNANjgKE0G6zKhdHnL29JHihY+nQb08UtKwvvF3motJoK/nmZpQg1cvS1TlIzicknyXMHMF9W5d4VT6XQf3Qb8" \
      "SZUFyBcnlbuHNnYBBn3i1s7fqGWDTPMDjeJDKEKEvEWcPTF2v8y+jurvpT41Bw/hrNX3jh2ix833j98GyeMJxZnllAuMiZktTJNha+N9tnEfOg" \
      "aTMqXp1pw+eg==:::Cm2S60BdWt+KQGMvrX7P6w=="
sign_in_url = "http://openlaw.cn/login"
data = {
    "_csrf": "7ab15f3c-4bc5-4ea0-ac8b-0d6c90ca77e7",
    "username": "aciyz2pa@dawin.com",
    "password": pwd,
    "code": "SUCUE",
    "_spring_security_remember_me": "true",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "Referer": "http://openlaw.cn/login.jsp",
}
sess.request("POST", url=sign_in_url, headers=headers)

sucue_url = "http://openlaw.cn/login.jsp?$=success"
sess.request("GET", url=sucue_url, headers=headers)

user_url = "http://openlaw.cn/user/"
sess.request("GET", url=user_url, headers=headers)

profile_url = "http://openlaw.cn/user/profile.jsp"
response = sess.request("GET", url=profile_url, headers=headers)
print(response.text)
