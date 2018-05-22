import redis
import pymysql
import requests
import json

import time


def get_task():
    info_byte = r_conn.spop("soufang:task")
    if info_byte:
        info = info_byte.decode("utf-8")
        info_dict = eval(info)
        return info_dict
    else:
        return None


def crawl(task_dict):
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko)"
                      " Version/11.0 Mobile/15A372 Safari/604.1",
    }
    url = "http://wlmq.sofang.com/saleesb/area/aa2463-ab4004"
    params = {
        "f": "h5",
        "page": "1",
    }
    response = requests.get(url=url, params=params, headers=headers, timeout=8)
    data = json.loads(response.text)

    if response.text != "[]":

        buildings = data["builds"]
        for build_info in buildings:
            build = build_info["_source"]
            # 字段
            house_id = build["id"]
            name = build["name"]
            provinceId = build['provinceId']
            cityId = build['cityId']
            cityAreaId = build['cityAreaId']
            subwayStation = build['subwayStation']
            spiderSource = build['spiderSource']
            address = build['address']
            rentCount = build['rentCount']
            saleCount = build['saleCount']

            buildPriceAvg = build['buildPriceAvg']
            buildPriceAvgUnit = build['buildPriceAvgUnit']
            salesStatusPeriods = build['salesStatusPeriods']

            price_data = time.strftime("%Y%m%d")

            print(house_id, name, provinceId, cityId, cityAreaId, subwayStation, spiderSource, address, rentCount, saleCount, buildPriceAvg, buildPriceAvgUnit, salesStatusPeriods, price_data, response.url)

            sql = "insert into soufang_price(house_id, name, provinceId, cityId, cityAreaId, subwayStation," \
                  " spiderSource, address, rentCount, saleCount, buildPriceAvg, buildPriceAvgUnit," \
                  " salesStatusPeriods, priceDate, source_href, city_name, area_name, street_name)" \
                  " VALUE ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                  "'{}','{}')".format(house_id, name, provinceId, cityId, cityAreaId, subwayStation,
                                      spiderSource, address, rentCount, saleCount, buildPriceAvg,
                                      buildPriceAvgUnit, salesStatusPeriods, price_data, response.url,
                                      task_dict["city_name"], task_dict["city_name"], task_dict["city_name"])
            m_cursor.execute(sql)
            m_conn.commit()


if __name__ == '__main__':
    print("Connect to redis...")
    r_pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    # 连接MySQL
    print("Connect to mysql...")
    m_conn = pymysql.connect(host="192.168.70.40", port=3306, user="root",
                             passwd="mysql", db="soufang", charset='utf8')
    m_cursor = m_conn.cursor()

    try:
        task = get_task()
        crawl(task)
    finally:
        m_cursor.close()
        m_conn.close()
        print("MySQL connection close")