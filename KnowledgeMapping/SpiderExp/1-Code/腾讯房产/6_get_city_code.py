import requests
from lxml import etree
import re
import json


url = "http://db.house.qq.com/index.php?mod=search&city=dg#LXNob3d0eXBlXzEtdW5pdF8xLWFsbF8tcGFnZV8xLUNBMV80Mjo1NTIkNTUy"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}

response = requests.get(url=url, headers=headers)

html = etree.HTML(response.text)

rs = html.xpath("//div[@class='scrollContent']/dl/dd/a")

items = []
for r in rs:
    item = dict()
    item['name'] = r.xpath("./text()")[0]
    item['code'] = r.xpath("./@href")[0].split("&city=")[1]
    items.append(item)


with open("./city_word_code.json", "w") as f:
    f.write(json.dumps(items, ensure_ascii=False))