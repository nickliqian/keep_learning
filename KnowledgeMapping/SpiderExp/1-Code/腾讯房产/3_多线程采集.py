import requests
import time
import re
import pymysql
import redis
import random
from lxml import etree
from constant import all_city_code_url


# MySQL
mysql_db = "lianjia"
mysql_table = "lianjia_area"
m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
m_cursor = m_conn.cursor()

# Redis
r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r_conn = redis.Redis(connection_pool=r_pool)

# Request params
url = "http://db.house.qq.com/index.php"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}
params = {
    "mod": "search",
    "act": "newsearch",
    "city": "sz",
    "showtype": "1",
    "page_no": "2",
    "CA": "1:5"
}


def to_chinese(string):
    return string.encode('utf-8').decode('unicode_escape')


# get proxy from redis wuyou api
def get_proxy_from_wuyou_api():
    while True:
        try:
            num_list = [k_i for k_i in range(1, 21)]
            ip_choice = random.choice(num_list)
            ip_str = "myip" + str(ip_choice)
            ip_num = r_conn.mget(ip_str)[0]
            if not ip_num:
                return None
            ip_num = ip_num.decode('utf-8')
            print("proxy: {}".format(ip_num))
            return ip_num
        except Exception as get_proxy_error:
            print(get_proxy_error)
            time.sleep(1)


def get_area_code(city_dict):
    param_city = city_dict["city_url"].split("?")[1].split("&")[1].split("=")[1]

    while True:
        try:
            response = requests.get(url=city_dict["city_url"], headers=headers, proxies={"http": get_proxy_from_wuyou_api()}, timeout=8)
            break
        except Exception:
            pass

    html = etree.HTML(response.text)
    areas = html.xpath("//dl[@id='search_condition_container_region']/dd/ul[@id='search_condition_region1']/li/a")

    # print("area_code, area_name---------------------------------")
    for area in areas:
        area_id = area.xpath("./@onclick")[0]
        all_id_string = re.findall(r"\s'(.*?)'\);", area_id)[0]
        area_code = all_id_string.split(":")[1]
        area_name = area.xpath("./text()")[0]
        param_CA = city_dict["city_code"]+":"+area_code


        req_area(param_city, param_CA, area_name, city_dict["city_name"])


def req_area(param_city, param_CA, area_name, city_name):
    params["city"] = param_city
    params["CA"] = param_CA

    # 获取第一页中的数字-数据总量
    params["page_no"] = "1"

    while True:
        try:
            response = requests.get(url=url, headers=headers, params=params, proxies={"http": get_proxy_from_wuyou_api()}, timeout=8)
            break
        except Exception:
            pass

    # 抽取文本
    results = re.findall(r'var\ssearch_result\s=\s"(.*?);var\ssearch_result_list_num\s=\s(.*?);', response.text)
    result = results[0]
    # 本分类总数
    count = int(result[1])

    # 计算页码
    page_num = int(count/10) + 1

    # 循环所有页面
    for num in range(1, page_num+1):
        params["page_no"] = str(num)
        response = requests.get(url=url, headers=headers, params=params)
        parse_resp(response, area_name, city_name)
        time.sleep(10)


def parse_resp(response, area_name, city_name):
    # 抽取文本
    results = re.findall(r'var\ssearch_result\s=\s"(.*?);var\ssearch_result_list_num\s=\s(.*?);', response.text)
    result = results[0]

    # 本分类总数
    # count = int(result[1])
    # html源码转换
    text = result[0].replace(r'\"', '"').replace(r"\/", "/")

    # lxml解析
    html = etree.HTML(text)
    buildings = html.xpath("//div[@class='textList fl']")

    for building in buildings:

        # 楼盘名称
        build_name = to_chinese(building.xpath(".//h2/a/text()")[0]).strip()

        # 楼盘链接
        build_name_href = to_chinese(building.xpath(".//h2/a/@href")[0]).strip()

        # 楼盘状态
        build_status = to_chinese(building.xpath(".//li[@class='title']/span/text()")[0]).strip()

        # 楼盘户型
        build_house_type_xpath = building.xpath(".//li[@class='h_type']/a/text()")
        if build_house_type_xpath:
            build_house_type = to_chinese("/".join(build_house_type_xpath)).strip()
        else:
            build_house_type = "暂无资料"

        # 楼盘地址
        build_address = to_chinese(building.xpath(".//li[@class='address']/@title")[0]).strip()
        if not build_address:
            build_address = to_chinese(building.xpath(".//li[@class='address']/a/text()")[0]).strip()

        # 楼盘标签
        build_tags_xpath = building.xpath(".//li[@class='tags']/a/text()")
        if build_tags_xpath:
            build_tags = to_chinese(",".join(build_tags_xpath)).strip()
        else:
            build_tags = "暂无标签"

        # 楼盘价格
        build_price_type = to_chinese(building.xpath(".//li[@class='title']/p[@class='fr']/text()")[0]).strip()
        build_price_price = to_chinese(building.xpath(".//li[@class='title']/p[@class='fr']/a/text()")[0]).strip()
        build_price_unit = to_chinese(building.xpath(".//li[@class='title']/p[@class='fr']/text()")[1]).strip()

        print("{}{}{}{}{}{}{}{}{}{}{}"
              .format(build_name, build_name_href, build_status,
                      build_house_type, build_address, build_tags,
                      build_price_type, build_price_price, build_price_unit, area_name, city_name
                      ))

        with open("./crawl_data.csv", "a+") as f:
            f.write("{},{},{},{},{},{},{},{},{},{},{}\n"
                .format(build_name, build_name_href, build_status,
                      build_house_type, build_address, build_tags,
                      build_price_type, build_price_price, build_price_unit, area_name, city_name
                      ))


# {'city_code': '279', 'city_name': '舟山', 'city_url': 'http://db.house.qq.com/index.php?mod=search&city=zhoushan'},
def main():
    for c_d in all_city_code_url:
        get_area_code(c_d)


if __name__ == '__main__':
    main()
