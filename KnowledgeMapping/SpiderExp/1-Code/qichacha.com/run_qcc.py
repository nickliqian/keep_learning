"""
循环采集企查查的公司名称
"""
import requests
from lxml import etree
import pymysql
import redis
import time
import random
from get_area_dict import write_area_dict


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


def req_page(area_dict, page_num):
    url = "http://www.qichacha.com/g_{}_{}.html".format(area_dict["code"], page_num)

    f = 1
    while True:
        if f > 3:
            return 0
        try:
            response = requests.get(url=url, headers=headers, timeout=6, proxies={"http": get_proxy()})
            return response
        except Exception as e:
            f += 1
            print("异常 {}".format(e))


def parse_page(resp, area_dict, page_num):
    html = etree.HTML(resp.text)
    results = html.xpath("//section[@id='searchlist']/a[@class='list-group-item clearfix']")

    for result in results:
        try:
            name = result.xpath("./span[@class='clear']/span[@class='name']/text()")[0]
            href = site + result.xpath("./@href")[0]
            print("{:<10}{:<18}{:^100}".format(area_dict["city"], name, href))
            sql = "INSERT IGNORE INTO qcc_com_name(company_name, desc_url, area, page) VALUE ('{}','{}','{}','{}')".format(
                name, href, area_dict["city"], page_num)
            mysql_cursor.execute(sql)
        except IndexError:
            pass
    mysql_conn.commit()


# 获取一个 city-url 字典
def get_task():
    area_b = redis_conn.spop("QCC:area_dict")
    if area_b:
        area = area_b.decode("utf8")
        return eval(area)
    else:
        print("redis 数据为空")
        write_area_dict()


if __name__ == '__main__':

    # 连接MySQL
    print("Connect to mysql...")
    mysql_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='qichacha', charset='utf8')
    mysql_cursor = mysql_conn.cursor()

    # 连接redis
    redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    redis_conn = redis.Redis(connection_pool=redis_pool)

    # 参数设置
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    site = "http://www.qichacha.com"

    try:
        while True:
            # 获取一个 city-url 字典
            area_b = get_task()
            print(area_b)
            if area_b != 0:
                for i in range(1, 501):
                    print("page <{}>".format(i))
                    r = req_page(area_b, i)
                    # time.sleep(0.2)
                    if r:
                        parse_page(r, area_b, i)
                    else:
                        print("采集失败 <{}> <{}>".format(area_b, i))
            else:
                break
    except Exception as e:
        raise e
    finally:
        # 关闭mysql连接
        mysql_cursor.close()
        mysql_conn.close()
        print("Close MySQL Connection...")
        print("end")