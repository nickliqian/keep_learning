import requests
import time
import json
import pymysql
from constant import city2code_dict


def timestamp2date(timestamp):
    return time.strftime("%Y%m%d", time.localtime(timestamp))


querystring = {
    "defaultCityName": "北京",
    "districtName": "",
    "region": "",
    "block": "",
    "keyword": "巷上嘉园"
}

headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
}


def save_data():
    pass


def crawl_curve(default_city_name, keyword, url_code):
    url = "http://{}.fangjia.com/trend/year2Data".format(url_code)
    querystring["defaultCityName"] = default_city_name
    querystring["keyword"] = keyword
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.text == "null":
        print("未查询到此数据 <{}> <{}> <{}>".format(default_city_name, keyword, url))
        return None

    content = json.loads(response.text)

    real_house_name = content["series"][0]["name"]
    price_list = content["series"][0]["data"]
    for stamp_price in price_list:
        evaluation_time = timestamp2date(stamp_price[0]/1000)
        price = stamp_price[1]
        print("{}  {}  {}  {}元/平米".format(default_city_name, real_house_name, evaluation_time, price))


if __name__ == '__main__':

    # 连接MySQL
    print("Connect to mysql...")
    mysql_db = "fangjiawang"
    m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
    m_cursor = m_conn.cursor()

    num_id = 1
    try:
        sql = "select * from house_name where id={}".format(num_id)
        m_cursor.execute(sql)
        query_results = m_cursor.fetchall()
        print(query_results)
        if not query_results:
            print("MySQL查询结果为空 id=<{}>".format(num_id))
        else:
            query_houses = query_results[0][2]
            query_city = query_results[0][1]
            query_url_code = city2code_dict[query_city]

            crawl_curve(query_city, query_houses, query_url_code)

    finally:
        m_cursor.close()
        m_conn.close()
        print("MySQL connection close...")