import requests
from lxml import etree

# url = "https://www.baidu.com/s"
#
# params = {
#     "wd": "15992410441"
# }
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}
#
# response = requests.get(url=url, headers=headers, params=params)
#
# html = etree.HTML(response.text)
# results = html.xpath("//div[@class='c-border op_fraudphone_container']/div//div[@class='op_fraudphone_word']")
#
# # 判断xpath结果是否为空，不为空则进一步解析并返回数据，否则返回None
# if results:
#     # 如果解析不到某个字段就置为-1
#     try:
#         mark_person = results[0].xpath("./text()")[0].strip().replace("被", "").replace("个", "")
#     except IndexError:
#         mark_person = "-1"
#     try:
#         tag = results[0].xpath("./strong/text()")[0].replace('"', '')
#     except IndexError:
#         tag = "-1"
#     try:
#         source_site = results[0].xpath("./a/text()")[0]
#     except IndexError:
#         source_site = "-1"
#     print("--")
#     print(mark_person, tag, source_site)


check_ip_res = requests.get(
                            url="https://www.baidu.com",
                            headers=headers,
                            proxies={"http": "117.78.31.36:1080", "https": "117.78.31.36:1080"},
                            verify=False,
                            timeout=5,
                            allow_redirects=False
                        )

print(check_ip_res)
print(check_ip_res.text)