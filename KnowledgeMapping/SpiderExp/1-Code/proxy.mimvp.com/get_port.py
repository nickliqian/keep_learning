import requests
from lxml import etree
import time


url = "https://proxy.mimvp.com/free.php?proxy=in_hp&sort=&page=1"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
}


r = requests.get(url=url, headers=headers)
r = r.text
#
with open("./mipu.html", "w") as f:
    f.write(r)

# print(r.text)

# with open("./mipu.html", "r") as f:
#     r = f.read()
html = etree.HTML(r)


ips = html.xpath("//table/tbody/td[@class='tbl-proxy-ip']")
ports = html.xpath("//table/tbody/td[@class='tbl-proxy-port']")
protocols = html.xpath("//table/tbody/td[@class='tbl-proxy-type']")
base_url = "https://proxy.mimvp.com/"


# print(len(ips))
# print(len(ports))
# print(len(protocols))


items = []
for i in range(20):
    item = {}
    item['ip'] = ips[i].xpath("./text()")[0]
    img_url = base_url + ports[i].xpath("./img/@src")[0]
    item['img_url'] = img_url
    item['protocols'] = protocols[i].xpath("./text()")[0].lower()
    r = requests.get(img_url)
    filename = "./img/" + str(i)+".png"
    with open(filename, "wb") as f:
        f.write(r.content)
        time.sleep(2)
