import requests
from lxml import etree


url = "https://gongshang.mingluji.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}

response = requests.get(url=url, headers=headers)
html = etree.HTML(response.text)

results = html.xpath("//table//tr[position()>1]")

for result in results:
    area = result.xpath("./td[1]/a/text()")[0].strip()
    number = result.xpath("./td[2]/text()")[0].strip()
    number = int(number)/100
    href = result.xpath("./td[3]/a/@href")[0].strip().strip("/")
    print(area, number, href)
