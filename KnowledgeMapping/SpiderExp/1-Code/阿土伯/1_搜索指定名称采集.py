# -*- coding:utf-8 -*-
import requests


url = "https://www.atobo.com.cn/GongShang/Search_Redirect.aspx"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}
data = {
    "Keyword": "上海神澳电子科技有限公司",
    "ktype": "1",
}

response = requests.post(url=url, headers=headers, data=data)

print(response.encoding)
response.encoding = "gb2312"

print(response.text)
