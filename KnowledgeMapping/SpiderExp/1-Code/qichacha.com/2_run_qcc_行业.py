"""
循环采集企查查的公司名称
"""
import requests
from lxml import etree
import pymysql
import redis
import time
import random
import json


def write_sort_info_to_redis():
    with open("./行业分类3.json", "r") as f:
        sort_dict = json.load(f)
    for sd in sort_dict:
        for s in sd:
            print("Insert to Redis - {}".format(s))
            redis_conn.sadd(redis_task_name, str(s))


def get_proxy():
    """
    获得代理IP
    :return: string
    """
    while True:
        try:
            num_list = [i for i in range(1, 21)]
            ip_choice = random.choice(num_list)
            ip_str = "myip" + str(ip_choice)
            ip_num = redis_conn.mget(ip_str)[0]
            if not ip_num:
                return None
            ip_num = ip_num.decode('utf-8')
            print("本次的代理为: %s" % ip_num)
            return ip_num
        except Exception as e:
            print(e)
            time.sleep(1)


def req_page(industry_dict, page_num):
    url = "http://www.qichacha.com/gongsi_industry.shtml"
    params = {
        "industryCode": industry_dict["big_sort_code"],
        "subIndustryCode": industry_dict["small_sort_code"],
        "p": str(page_num),
    }

    f = 1
    while True:
        if f > 3:
            return 0
        try:
            response = requests.get(url=url, headers=headers, params=params, timeout=6, proxies={"http": get_proxy()})
            if response.text.startswith("<script>") or response.text.startswith("<html><head><title>too many request"):
                print("request again")
                time.sleep(0.5)
            else:
                return response
        except Exception as e:
            f += 1
            print("异常 {}".format(e))


def parse_page(resp, industry_dict, page_num):
    html = etree.HTML(resp.text)
    results = html.xpath("//section[@id='searchlist']/a[@class='list-group-item clearfix']")
    print("解析结果 {}".format(results))
    if not results:
        with open("./req_log.html", "w") as f:
            print("记录log")
            f.write(resp.text)

    for result in results:
        try:
            name = result.xpath("./span[@class='clear']/span[@class='name']/text()")[0]
            href = site + result.xpath("./@href")[0]

            print("{} {} {} {}".format(industry_dict["big_sort_name"], industry_dict["small_sort_name"], name, href))
            sql = "INSERT IGNORE INTO qcc_industry(company_name,desc_url,page,big_sort_name,small_sort_name)" \
                  " VALUE ('{}','{}','{}','{}','{}')"\
                .format(name, href, page_num, industry_dict['big_sort_name'], industry_dict['small_sort_name'])
            mysql_cursor.execute(sql)
        except IndexError:
            print("Index Error {}".format(str(industry_dict)))
            pass
    mysql_conn.commit()


# 获取一个 city-url 字典
def get_task():
    info_byte = redis_conn.spop(redis_task_name)
    if info_byte:
        info = info_byte.decode("utf8")
        return eval(info)
    else:
        print("redis 数据为空")
        write_sort_info_to_redis()
        get_task()


if __name__ == '__main__':

    # 连接MySQL
    print("Connect to mysql...")
    mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='qichacha', charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    # 连接redis
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    redis_conn = redis.Redis(connection_pool=redis_pool)
    redis_task_name = "QCC:industry"

    # 参数设置
    headers = {
        'Host': "www.qichacha.com",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'Accept-Language': "en-GB,en;q=0.5",
        'Accept-Encoding': "gzip, deflate, br",
        'Referer': "https://www.qichacha.com/",
        'Cookie': "PHPSESSID=ru60bhoufj1lhg1m3sjfftj4q1; zg_did=%7B%22did%22%3A%20%22163a46c367a158-0ddfd0ff3b2e0d-77256752-1fa400-163a46c367bc4%22%7D; zg_de1d1a35bfa24ce29bbf2c7eb17e6c4f=%7B%22sid%22%3A%201527475246083%2C%22updated%22%3A%201527475468455%2C%22info%22%3A%201527471945343%2C%22superProperty%22%3A%20%22%7B%7D%22%2C%22platform%22%3A%20%22%7B%7D%22%2C%22utm%22%3A%20%22%7B%7D%22%2C%22referrerDomain%22%3A%20%22www.qichacha.com%22%2C%22cuid%22%3A%20%2233799dc8c55df5d568574fe8b8e6d743%22%7D; Hm_lvt_3456bee468c83cc63fb5147f119f1075=1527471946,1527475469; Hm_lpvt_3456bee468c83cc63fb5147f119f1075=1527475469; hasShow=1; acw_tc=AQAAAL3ktQTl5woAahZ0cSZmyE+sfgTk; _uab_collina=152747224744409167053837; _umdata=65F7F3A2F63DF020D87880E9B80A96A075249762FF74E57905ED55924DBB6DCB2C9C029F1779208CCD43AD3E795C914C952A43E8A7CBBE835A6FD6035C591050",
        'DNT': "1",
        'Cache-Control': "no-cache",
    }

    site = "http://www.qichacha.com"

    try:
        while True:
            # 获取一个 city-url 字典
            row = get_task()
            print("get from redis -> {}".format(row))
            if row:
                for i in range(1, 501):
                    print("page <{}>".format(i))
                    r = req_page(row, i)
                    time.sleep(1)
                    if r:
                        print("开始解析")
                        parse_page(r, row, i)
                    else:
                        print("采集失败 <{}> <{}>".format(row, i))
                    time.sleep(5)
    except Exception as e:
        raise e
    finally:
        # 关闭mysql连接
        mysql_cursor.close()
        mysql_conn.close()
        print("Close MySQL Connection...")
        print("end")