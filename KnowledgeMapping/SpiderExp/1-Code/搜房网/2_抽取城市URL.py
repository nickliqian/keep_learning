from lxml import etree
import json


with open("./抽取城市URL.html", "r") as f:
    content = f.read()


html = etree.HTML(content)

results = html.xpath("/html/body/div[3]/hgroup/a")

items = []
for i in range(1, len(results)):
    item = dict()
    item['city_url'] = results[i].xpath("./@href")[0]
    item['city_name'] = results[i].xpath("./h4/text()")[0]
    items.append(item)

data = json.dumps(items, ensure_ascii=False)
with open("./city_map.json", "w") as f:
    f.write(data)