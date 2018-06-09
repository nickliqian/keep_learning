import requests
from lxml import etree
import time
import pymysql
import threading


def get_proxy():
    url = "http://47.106.170.4:8081/Index-generate_api_url.html?packid=1000&fa=0&qty=1&port=1&format=txt&ss=3&css=&ipport=1&pro=&city="

    while True:
        response = requests.get(url=url)
        if "请求太频繁" in response.text:
            print(response.text)
        else:
            print(response.text)
            return response.text.strip()


print("Connect to mysql...")
m_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db="mingluji", charset='utf8')
m_cursor = m_conn.cursor()

url_location = "tianjin"
area_name = "天津"

base = "https://gongshang.mingluji.com"
url = "https://gongshang.mingluji.com/{}/list".format(url_location)
query_string = {
    "page": "1",
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}

# ip = get_proxy()

try:

    for i in range(171, 10000):
        while True:
            try:
                print(">>> {}".format(i))
                source_href = "https://gongshang.mingluji.com/{}/list" + "?page={}".format(url_location, i)
                query_string["page"] = str(i)
                response = requests.get(url=url, params=query_string, headers=headers, timeout=8, proxies={"https": None})
                break
            except:
                # ip = get_proxy()
                time.sleep(2)

        html = etree.HTML(response.text)
        results = html.xpath("//div[@class='item-list']/ol/li/div[@class='views-field views-field-title']/span[@class='field-content']/a")
        if not results:
            print("break {}".format(i))
            break
        for result in results:
            name = result.xpath("./text()")[0]
            href = result.xpath("./@href")[0]
            print(name, base+href)

            sql = "insert into company_list(name, url, area, source_href) VALUE (%s, %s, %s, %s)"
            m_cursor.execute(sql, [name, base+href, area_name, source_href])
        m_conn.commit()
        # time.sleep(0.1)

finally:
    m_cursor.close()
    m_conn.close()
    print("MySQL connection close...")
