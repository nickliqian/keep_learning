#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests


sess = requests.Session()
url = "http://openlaw.cn/register.jsp"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
}
response = sess.get(url=url, headers=headers)
print(response.cookies.items())

url = "http://openlaw.cn/Kaptcha.jpg?v=1531924553758"
response = sess.get(url=url, headers=headers)
with open("./p.png", "wb") as f:
    f.write(response.content)
print(response.cookies.items())


"""
POST http://openlaw.cn/service/rest/us.User/collection/register HTTP/1.1
Host: openlaw.cn
Connection: keep-alive
Content-Length: 170
Pragma: no-cache
Cache-Control: no-cache
Accept: */*
Origin: http://openlaw.cn
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://openlaw.cn/register.jsp
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: SESSION=ZDE4OWY1YjAtZDE3My00YmQ0LWI1YjctMmY5M2JjZDQ5ZmI0; Hm_lvt_a105f5952beb915ade56722dc85adf05=1531923793; Hm_lpvt_a105f5952beb915ade56722dc85adf05=1531924090

_csrf=7ab15f3c-4bc5-4ea0-ac8b-0d6c90ca77e7
email=jbweosaz%40dawin.com
userName=jbweosaz%40dawin.com
nickName=jbweosaz
password=1qaz%40WSX
validateCode=7zckz
agree=forever
"""