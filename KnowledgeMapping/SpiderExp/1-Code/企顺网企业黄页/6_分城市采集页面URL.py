import pymysql
import requests
import json
import time
from lxml import etree


def req_area_url():
    domain = "http://www.11467.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    with open("./a地域列表.json", "r") as f:
        all_area = json.load(f)

    start = False
    for area in all_area:
        city_name = area["name"].strip()
        url = domain + area["href"] + "/"
        print(city_name, url)

        if city_name == "文山":
            start = True

        if start:

            response = requests.get(url=url, headers=headers, proxies={"http": "117.78.31.36:1080"}, timeout=20)
            parse_city_page(response, city_name)

            time.sleep(3.5)


def parse_city_page(response, city_name):

    def parse_a(ele_lis):
        for a in ele_lis:
            href = a.xpath("./@href")[0].strip().strip("//")
            if not href.startswith("http://"):
                href = "http://" + href
            title = a.xpath("./text()")[0].strip().strip(city_name).replace("黄页", "")
            # print(city_name, href, title)
            sql = "insert ignore into request_index(city, url_title, url) VALUE ('{}','{}','{}')"\
                .format(city_name, title, href)
            mysql_cursor.execute(sql)
        mysql_conn.commit()

    html = etree.HTML(response.text)

    type_1 = html.xpath("/html/body/div[@id='main']/div[@id='il']/div[@class='box  huangyecity t5'][1]/"
                        "div[@class='boxcontent']/ul[@class='listtxt']/li/dl/dd/a")
    parse_a(type_1)

    type_2 = html.xpath("/html/body/div[@id='main']/div[@id='il']/div[@class='box  huangyecity t5'][2]/"
                        "div[@class='boxcontent']/ul[@class='listtxt']/li/dl/dd/a")
    parse_a(type_2)

    type_3 = html.xpath("/html/body/div[@id='main']/div[@id='il']/div[@class='box sidesubcat t5'][1]/"
                        "div[@class='boxcontent']/dl[@class='listtxt']/dd/a")
    parse_a(type_3)

    type_4 = html.xpath("/html/body/div[@id='main']/div[@id='il']/div[@class='box sidesubcat t5'][2]/"
                        "div[@class='boxcontent']/dl[@class='listtxt']/dd/a")
    parse_a(type_4)

    type_5 = html.xpath("/html/body/div[@id='main']/div[@id='il']/div[@class='box sidesubcat t5'][3]/"
                        "div[@class='boxcontent']/dl[@class='listtxt']/dd/a")
    parse_a(type_5)

    print("{:5} {:5} {:5} {:5} {:5}".format(len(type_1), len(type_2), len(type_3), len(type_4), len(type_5)))


if __name__ == '__main__':

    print("Connect to mysql...")
    mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='qishun',
                                 charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    try:
        print("工商黄页分类", "公司分类", "热门行业分类", "热门公司分类", "按地区浏览")
        req_area_url()

    finally:
        mysql_cursor.close()
        mysql_conn.close()
        print("Close MySQL Connection...")
        print("end")
