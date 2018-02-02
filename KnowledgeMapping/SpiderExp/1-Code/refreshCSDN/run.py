import requests
from lxml import etree

# list page = 1 2 3 --> 0
# csdn_id = ""
url = "http://blog.csdn.net/weixin_39198406/article/list/"  # + page

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Host": "blog.csdn.net",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://blog.csdn.net/weixin_39198406",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",

}

r = requests.get(url, headers=headers)
print(r)

# //li[@class='blog-unit']/a/@href
