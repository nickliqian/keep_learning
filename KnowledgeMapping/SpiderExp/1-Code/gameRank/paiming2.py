import requests
from lxml import etree
import time



def to_chinese(string):
    return string.encode('utf-8').decode('unicode_escape')


with open("file.csv", "w") as f:
    pass

url = "https://www.taptap.com/ajax/top/played"

querystring = {"page": "1", "total": "30"}

headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'Cache-Control': "no-cache",
    'Connection': "keep-alive",
    'Cookie': "acw_tc=AQAAALBXkmdQNA8AKnFYcSO32i/Mwy1E; region=eyJpdiI6ImswOGx5Sklia21QWmFWTHlZbFVnVXc9PSIsInZhbHVlIjoiMFlTZjVCc3VuaEwrNElxeEVnV1lNdz09IiwibWFjIjoiMTQ4MGY2NGE3OWVjZTRkY2JlOTI0MDc5NGJkYjE3ODk0YmE3NzAwMTMwNDg1MzBlZDZjZmI0NmQ4YWEzYmI4ZCJ9; _ga=GA1.2.1241898569.1527750258; _gid=GA1.2.1300165587.1527750258; OUTFOX_SEARCH_USER_ID_NCOO=624446872.5091474; _gat=1; XSRF-TOKEN=eyJpdiI6Ijd3N24zTjR1MjFqdFhZZUdlWXo2eUE9PSIsInZhbHVlIjoiZ282QzNEUVZBd1FQSkxTYXdaYmxCbXZJVThNUGtOOTNTM09DTmhaSnlTU3BLeUxIRmtZNlZsOWx3RHc3MTI1QllsUHY4NnFGU082REEybG5uZTJhVHc9PSIsIm1hYyI6IjIzZmE5YzQwMzViZDdjNTgyNzg2YjliMTkwNzZjNmZhN2E3ZDA4MmMzODg3MmZlMDU0NWNjOGU0M2U5NTY2NTYifQ%3D%3D; tap_sess=eyJpdiI6IkM2aUZoaXROV0RtU1lBa04rakUzS2c9PSIsInZhbHVlIjoiSDFcL3lnY3NCRlJBUEVYa3RQOWlmK0Q3bWUyNnZSVkgwSUlqaWJNZTZjRGsxNW1MMWlQSWxPamFmNUJsb3RmazY1eVM0TnYzQ2JRaWZcL3V5bmtLaUFKdz09IiwibWFjIjoiMzQ0ZjMxYjlhMzQ1Mjk1MTNjNWVmYTYzNDcxOTBjMDRjODY5NjU0YzJlZDc3MWQ4NTI1YTMxZGIzMGJkMTdhZSJ9",
    'Host': "www.taptap.com",
    'Pragma': "no-cache",
    'Referer': "https://www.taptap.com/top/played",
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest",
    'X-XSRF-TOKEN': "eyJpdiI6Ijd3N24zTjR1MjFqdFhZZUdlWXo2eUE9PSIsInZhbHVlIjoiZ282QzNEUVZBd1FQSkxTYXdaYmxCbXZJVThNUGtOOTNTM09DTmhaSnlTU3BLeUxIRmtZNlZsOWx3RHc3MTI1QllsUHY4NnFGU082REEybG5uZTJhVHc9PSIsIm1hYyI6IjIzZmE5YzQwMzViZDdjNTgyNzg2YjliMTkwNzZjNmZhN2E3ZDA4MmMzODg3MmZlMDU0NWNjOGU0M2U5NTY2NTYifQ==",
    'Postman-Token': "17cca2dd-55cf-43bd-8fbe-71e2f2833abd"
}

j = 1
for i in range(1, 5):
    querystring["page"] = str(i)
    response = requests.request("GET", url, headers=headers, params=querystring, timeout=6)


    text = response.text.strip('{"success":true,"data":{"html":"').strip('"}}').replace("\/", "/").replace(r'\"', '"')
    print(response)
    print(text)

    result = etree.HTML(text)

    rs = result.xpath("/html/body/div[@class='taptap-top-card']")

    print(rs)

    for r in rs:
        item = {}
        item["rank"] = r.xpath("./span[@class='top-card-order-text']/text()")[0]
        item["name"] = r.xpath("./div[@class='top-card-middle']/a[@class='card-middle-title ']/h4/text()")
        if not item["name"]:
            item["name"] = r.xpath(
                "./div[@class='top-card-middle']/a[@class='card-middle-title hasArea']/h4/text()")
        item["name"] = item["name"][0]

        item["company"] = r.xpath("./div[@class='top-card-middle']/p[@class='card-middle-author']/a/text()")[0]
        item["type"] = r.xpath("./div[@class='top-card-middle']/div[@class='card-middle-footer']/a/text()")[0]
        item["point"] = r.xpath(
            "./div[@class='top-card-middle']/div[@class='card-middle-footer']/p[@class='middle-footer-rating']/span/text()")[
            0]

        print(item)
        with open("file.csv", "a+") as f:
            s = [str(j), to_chinese(item["name"]), to_chinese(item["company"]), to_chinese(item["type"]), to_chinese(item["point"])]
            s = ",".join(s)
            f.write(s + "\n")
            j += 1

        # time.sleep(5)