import requests
from lxml import etree


url = "https://www.kuaidaili.com/free/inha/1/"
# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
}

# 发送请求
response = requests.get(url, headers=headers)

# 解析页面源码
html = etree.HTML(response.text)
trs = html.xpath("//div[@id='list']/table//tr[position()>1]")
for tr in trs:
    ip = tr.xpath("./td[1]/text()")[0]
    port = tr.xpath("./td[2]/text()")[0]
    feature = tr.xpath("./td[3]/text()")[0]
    protocol = tr.xpath("./td[4]/text()")[0]
    location = tr.xpath("./td[5]/text()")[0]
    speed = tr.xpath("./td[6]/text()")[0]
    verify_time = tr.xpath("./td[7]/text()")[0]
    # 数据写入到文件
    with open("./data.csv", "a+") as f:
        ele_list = [ip, port, feature, protocol, location, speed, verify_time]
        print(">>> Write to file >>> {}".format(ele_list))
        s = ",".join(ele_list) + "\n"
        f.write(s)
