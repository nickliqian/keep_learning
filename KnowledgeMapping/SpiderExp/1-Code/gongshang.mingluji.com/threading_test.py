import random

import requests
from lxml import etree
import time
import pymysql
import threading
import redis


class CrawlList(threading.Thread):
    def __init__(self, mysql_conn, mysql_cursor, redis_conn, threading_lock):
        super(CrawlList, self).__init__()
        # 线程参数
        self.threading_lock = threading_lock
        self.stop_flag = False
        # 请求参数
        # self.ip = self.get_proxy()
        self.base = "https://gongshang.mingluji.com"
        self.query_string = {
            "page": "1",
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
        }
        # MySQL
        self.mysql_conn = mysql_conn
        self.mysql_cursor = mysql_cursor
        # Redis
        self.redis_conn = redis_conn
        self.redis_db = "mingluji"

    # 从redis获取代理IP
    def get_proxy(self):
        while True:
            try:
                num_list = [i for i in range(1, 21)]
                ip_choice = random.choice(num_list)
                ip_str = "myip" + str(ip_choice)
                ip_num = self.redis_conn.mget(ip_str)[0]
                if not ip_num:
                    return None
                ip_num = ip_num.decode('utf-8')
                print("proxy: %s" % ip_num)
                return ip_num
            except Exception as e:
                print(e)
                time.sleep(1)

    # 停止运行
    def stop(self):
        print("停止标志 -> stop_flag = True")
        self.stop_flag = True

    # 获取redis任务
    def get_task(self):
        # ('湖北', '10519', 'hubei')
        info_byte = self.redis_conn.spop(self.redis_db)
        if info_byte:
            info = info_byte.decode("utf-8")
            info_dict = eval(info)
            return info_dict
        else:
            return None

    def req_url(self, area, number, mark):
        while not self.stop_flag:
            try:
                print(">>> {} {} {}".format(area, number, mark))
                self.query_string["page"] = str(number)
                url = "https://gongshang.mingluji.com/{}/list".format(mark)
                response = requests.get(url=url, params=self.query_string,
                                        headers=self.headers, timeout=30,
                                        verify=False, proxies={"https": self.get_proxy()})
                return response
            except Exception as req_url_error:
                time.sleep(1)
                print("requests error: {}".format(req_url_error))

    def run(self):
        while not self.stop_flag:
            task_dict = self.get_task()
            if not task_dict:
                print("redis is empty, break")
                break

            area = task_dict[0]
            number = task_dict[1]
            mark = task_dict[2]

            try:
                response = self.req_url(area, number, mark)

                html = etree.HTML(response.text)
                results = html.xpath("//div[@class='item-list']/ol/li/div[@class='views-field views-field-title']/span[@class='field-content']/a")
                if not results:
                    print("break {}".format(self.query_string))
                    self.redis_conn.sadd(self.redis_db, task_dict)
                for result in results:
                    name = result.xpath("./text()")[0]
                    href = result.xpath("./@href")[0]
                    print(name, self.base + href)
                    sql = "insert into company_list(name, url, area, source_href) VALUE (%s, %s, %s, %s)"

                    with self.threading_lock:
                        source_url = "https://gongshang.mingluji.com/{}/list" + "?page={}".format(mark, number)
                        self.mysql_cursor.execute(sql, [name, self.base + href, area, source_url])
                        self.mysql_conn.commit()
            except Exception:
                print("task rollback to redis {}".format(task_dict))
                self.redis_conn.sadd(self.redis_db, task_dict)


def main():
    print("Connect to mysql...")
    mysql_db = "mingluji"
    m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
    m_cursor = m_conn.cursor()

    # 连接redis
    print("Connect to redis...")
    r_pool = redis.ConnectionPool(host="192.168.70.40", port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    # 线程列表
    threading_lock = threading.Lock()
    thread_num = 8
    job_list = []
    try:
        for i in range(thread_num):
            t = CrawlList(m_conn, m_cursor, r_conn, threading_lock)
            t.start()
            job_list.append(t)
        for t in job_list:
            t.join()
    except KeyboardInterrupt as e:
        # 手动停止时,执行所有对象的stop函数
        if job_list:
            for t in job_list:
                t.stop()
    except Exception as e:
        raise e
    finally:
        m_cursor.close()
        m_conn.close()
        time.sleep(25)
        print("MySQL connection close...")


if __name__ == '__main__':
    main()