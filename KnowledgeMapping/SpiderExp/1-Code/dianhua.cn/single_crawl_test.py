import requests
from lxml import etree


url = "http://www.dianhua.cn/search/yp?key=15999999999"

params = {
    "key": "13590242032"
}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

sess = requests.session()
sess.trust_env = False

response = sess.get(url=url, headers=headers)

print(response.encoding)
response.encoding = "utf-8"

with open("./data", "w") as f:
    f.write(response.text)


print(response.content.decode("utf-8"))
print(response.status_code)

html = etree.HTML(response.text)
result = html.xpath("//div[@class='c_right_body']/div[@class='c_right_list']/dl/dt[1]/h5/a/text()")
print(result)
