import requests
from lxml import etree
import time
import pymysql
import threading
import redis


class CrawlList(threading.Thread):
    def __init__(self, url_location, area_name, mysql_conn, mysql_cursor, redis_conn, threading_lock):
        super(CrawlList, self).__init__()
        # 线程参数
        self.threading_lock = threading_lock
        self.stop_flag = False
        # 请求参数
        # self.ip = self.get_proxy()
        self.url_location = url_location
        self.area_name = area_name
        self.base = "https://gongshang.mingluji.com"
        self.url = "https://gongshang.mingluji.com/{}/list".format(self.url_location)
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
        self.redis_db = "mingluji_task"

    @staticmethod
    def get_proxy():
        url = "http://127.0.0.1:7865/random_https"
        while True:
            try:
                response = requests.get(url=url)
                return response.text.strip()
            except:
                pass

    # 停止运行
    def stop(self):
        print("停止标志 -> stop_flag = True")
        self.stop_flag = True

    # 获取redis任务
    def get_task(self):
        info_byte = self.redis_conn.spop(self.redis_db)
        if info_byte:
            info = info_byte.decode("utf-8")
            info_dict = eval(info)
            return info_dict
        else:
            return None

    def req_url(self, task_number):
        while not self.stop_flag:
            try:
                print(">>> {}".format(task_number))
                self.query_string["page"] = str(task_number)
                response = requests.get(url=self.url, params=self.query_string, headers=self.headers, timeout=30)
                return response
            except Exception as req_url_error:
                # ip = self.get_proxy()
                time.sleep(2)
                print("requests error: {}".format(req_url_error))

    def run(self):
        while not self.stop_flag:
            task_number = self.get_task()
            if not task_number:
                print("redis is empty")
                break

            response = self.req_url(task_number)

            html = etree.HTML(response.text)
            results = html.xpath("//div[@class='item-list']/ol/li/div[@class='views-field views-field-title']/span[@class='field-content']/a")
            if not results:
                print("break {}".format(self.query_string))
                self.redis_conn.sadd(self.redis_db, task_number)
            for result in results:
                name = result.xpath("./text()")[0]
                href = result.xpath("./@href")[0]
                print(name, self.base + href)
                sql = "insert into company_list(name, url, area, source_href) VALUE (%s, %s, %s, %s)"

                with self.threading_lock:
                    source_url = "https://gongshang.mingluji.com/{}/list" + "?page={}".format(self.url_location, task_number)
                    self.mysql_cursor.execute(sql, [name, self.base + href, self.area_name, source_url])
                    self.mysql_conn.commit()


def main():
    print("Connect to mysql...")
    mysql_db = "mingluji"
    m_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
    m_cursor = m_conn.cursor()

    # 连接redis
    print("Connect to redis...")
    r_pool = redis.ConnectionPool(host="127.0.0.1", port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    # 请求参数
    url_location = "tianjin"
    area_name = "天津"

    # 线程列表
    threading_lock = threading.Lock()
    thread_num = 3
    job_list = []
    try:
        for i in range(thread_num):
            t = CrawlList(url_location, area_name, m_conn, m_cursor, r_conn, threading_lock)
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