import requests
from lxml import etree
import csv


url = "http://panyu.goodjob.cn/job/pos970735.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
}

r = requests.get(url=url)
html = etree.HTML(r.text)
lis = html.xpath("//ul[@class='c6']/li/text()")
item = {}
for li in lis:
    content = li.split("：")
    if len(content) == 1:
        content.append("NULL")
    item[content[0]] = content[1]
print(item)

with open("data.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(item.keys())
    writer.writerow(item.values())

