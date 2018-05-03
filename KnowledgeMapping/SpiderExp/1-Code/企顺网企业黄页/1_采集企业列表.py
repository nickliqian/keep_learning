
"""
从redis获取任务采集企顺网企业姓名，main程序
"""
import os
import pymysql
import requests
from lxml import etree
import time
import random
import redis
import threading


class RequestError(Exception):
    pass


class CrawlCampanyName(threading.Thread):

    def __init__(self, process_id, threading_name, mysql_conn, mysql_cursor, redis_conn, threading_lock):
        super(CrawlCampanyName, self).__init__()
        # 进程线程参数
        self.process_id = process_id
        self.threading_name = threading_name
        self.threading_lock = threading_lock
        self.stop_flag = False

        # 数据库连接
        self.mysql_conn = mysql_conn
        self.mysql_cursor = mysql_cursor
        self.mysql_db = "qishun"
        self.mysql_table = "qishun_company_name"
        self.redis_conn = redis_conn
        self.redis_db = "qishun_list"

        # 网络请求参数
        self.domain = "http://www.11467.com"
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    # 返回标准时间
    @staticmethod
    def get_now_time():
        time_obj = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return str(time_obj)

    # 停止运行
    def stop(self):
        print("停止标志 -> stop_flag = True")
        self.stop_flag = True

    # 向公共log文件中添加log信息
    def add_log(self, desc):
        with self.threading_lock:
            with open("./crawl.log", "a+") as f:
                f.write("T:<{}> P:<{}> T:<{}> D:<{}>\n".format(self.get_now_time(), self.process_id, self.threading_name, desc))

    # 获取redis任务
    def get_task(self):
        info_byte = self.redis_conn.spop(self.redis_db)
        if info_byte:
            info = info_byte.decode("utf-8")
            info_dict = eval(info)
            return info_dict
        else:
            return None

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

    # 插入数据库
    def insert_sql(self, items, row):
        for item in items:
            sql = "INSERT INTO {} (area,industry,source_url,company_name,company_url) VALUE ('{}','{}','{}','{}','{}')"\
                .format(self.mysql_table, row["area"], row["industry"], row["url"], item["name"], item["href"])
            self.mysql_cursor.execute(sql)
            print("Write data <{}> <{}> <{}> <{}> <{}>".format(row["area"], row["industry"], row["url"], item["name"], item["href"]))
        self.mysql_conn.commit()

    # 请求指定url（企顺网）
    def req_url(self, target_url):
        time.sleep(0.5)
        f = 0
        while f < 3:
            try:
                response = requests.get(url=target_url, headers=self.headers, proxies={"http": self.get_proxy()}, timeout=8)
                text = response.text
                if response.status_code == 200:
                    if (text.startswith("采集大神饶命")) or ("too many request" in text) or "":
                        time.sleep(1)
                        raise RequestError("请求太频繁，将放回redis队列重新请求")

                    if text.startswith("没找到"):
                        print("页面没有数据：没找到 {}".format(target_url))
                        return None

                    return response
                else:
                    print("状态码异常：{},{},{}\n".format(self.get_now_time(), target_url, response.status_code))
                    f += 1
            except Exception as e:
                print("请求异常：{},{},{}\n".format(self.get_now_time(), target_url, e))
                f += 1
        self.add_log("Request value<{}> failed".format(target_url))
        return None

    # 解析页面数据
    def parse_page(self, response):
        items = []
        html = etree.HTML(response.text)

        # 抽取公司名称
        results = html.xpath("//div[@class='f_l']/h4/a")
        print("{} 本次抓取公司名称<{}>个 {}".format(self.get_now_time(), len(results), response.url))
        if results:
            for result in results:
                item = {}
                name = result.xpath("./text()")[0].strip()
                href = result.xpath("./@href")[0].strip("//")
                if not href.startswith("http://"):
                    href = "http://" + href
                item["name"] = name
                item["href"] = href
                items.append(item)
        else:
            print("{} 本分类本页无公司 {}".format(self.get_now_time(), response.url))
            return items, 0

        # 判断是否有下一页
        results = html.xpath("//div[@class='pages']/a/em/../following-sibling::*[1]")
        if results:
            result = results[0]
            flag = result.xpath("./text()")[0]
            print("下一个标签是 <{}>".format(flag))
            if flag != "尾页":
                href = result.xpath("./@href")[0].strip("//")
                if not href.startswith("http://"):
                    href = "http://" + href
            else:
                print("{} 已经是最后一页 {}".format(self.get_now_time(), response.url))
                return items, 1
        else:
            print("{} 本分类仅一页 {}".format(self.get_now_time(), response.url))
            return items, 1

        return items, href

    # 采集某类企业
    def crawl_classification(self, response, row):

        items, href = self.parse_page(response)
        if href == 0:
            # print("本分类无公司")
            pass
        elif href == 1:
            # print("已经是最后一页")
            # 数据保存
            with self.threading_lock:
                self.insert_sql(items, row)
        else:
            # 数据保存
            with self.threading_lock:
                self.insert_sql(items, row)
            # 请求下一页
            response = self.req_url(href)
            if response:
                self.crawl_classification(response, row)
            else:
                print("{} 页面异常或者为空，无需解析 {}".format(self.get_now_time(), response.url))

    # Start
    def run(self):
        while not self.stop_flag:
            # 获取任务
            row = self.get_task()
            print("Start task {}".format(row))

            try:
                if row:
                    resp = self.req_url(row["url"])
                    if resp:
                        self.crawl_classification(resp, row)
                    else:
                        print("页面异常或者为空，无需解析")
                else:
                    print("Redis has no task")
            except Exception as e:
                self.redis_conn.sadd(self.redis_db, row)
                if isinstance(e, RequestError):
                    pass
                else:
                    self.add_log("{}--{}--{}--{}--{}".format(self.get_now_time(), self.process_id, self.threading_name, str(row), e))

        print("{} {} 线程退出".format(self.get_now_time(), self.threading_name))


if __name__ == '__main__':
    # 连接redis
    print("Connect to redis...")
    r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    # 连接MySQL
    print("Connect to mysql...")
    mysql_db = "qishun"
    m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
    m_cursor = m_conn.cursor()

    # 线程数量
    thread_num = 8
    # 线程锁
    t_lock = threading.Lock()
    # 线程列表
    jobList = []
    try:
        for i in range(thread_num):
            t_name = "Thread-" + str(i+1)
            t = CrawlCampanyName(os.getpid(), t_name, m_conn, m_cursor, r_conn, t_lock)
            t.start()
            jobList.append(t)
        for t in jobList:
            t.join()
    except KeyboardInterrupt as e:
        # 手动停止时,执行所有对象的stop函数
        if jobList:
            for t in jobList:
                t.stop()
    except Exception as e:
        # info_by_mail(">> gd spider stop", "进程报错 >> {}: {}".format(type(e), e))
        raise e
    finally:
        m_cursor.close()
        m_conn.close()
        time.sleep(25)
        print("进程 {} 已经退出".format(os.getpid()))