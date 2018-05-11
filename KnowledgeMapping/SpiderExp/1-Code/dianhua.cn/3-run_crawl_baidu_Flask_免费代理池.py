"""
从redis获取任务采集百度电话号码标记，main程序 >>> 无忧代理接口
"""
import os
import pymysql
import requests
from lxml import etree
import time
import random
import redis
import threading


class CrawlTelephone(threading.Thread):

    def __init__(self, process_id, threading_name, mysql_conn, mysql_cursor, redis_conn, threading_lock):
        super(CrawlTelephone, self).__init__()
        # 进程线程参数
        self.process_id = process_id
        self.threading_name = threading_name
        self.threading_lock = threading_lock
        self.stop_flag = False

        # 数据库连接
        self.mysql_conn = mysql_conn
        self.mysql_cursor = mysql_cursor
        self.redis_conn = redis_conn
        self.redis_db = "telephone_task"

        # 网络请求参数
        self.url = "https://www.baidu.com/s"
        self.params = {"wd": "1388888888"}
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

    # 获取redis任务数字-号码前缀数据的id
    def get_task(self):
        info_id_byte = self.redis_conn.spop(self.redis_db)
        if info_id_byte:
            info_id = info_id_byte.decode("utf-8")
            info_id = eval(info_id)
            return info_id
        else:
            return None

    # 返回数据库号码前缀查询结果
    def search_mysql(self, row_id):
        sql = "SELECT prefix FROM number_prefix WHERE id=%d" % int(row_id)
        with self.threading_lock:
            self.mysql_cursor.execute(sql)
            result = self.mysql_cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    # 从redis获取代理IP
    def get_proxy(self):
        """
        获得代理IP >>> 开源免费代理池
        :return: string
        """
        while True:
            try:
                r = requests.get("http://192.168.70.40:5555/random")
                ip_num = r.text
                print("本次的代理为: %s" % ip_num)
                return ip_num
            except Exception as e:
                print(e)
                time.sleep(1)

    def req_number(self, number):
        self.params["wd"] = number
        f = 0
        while f < 3:
            try:
                response = requests.get(url=self.url, headers=self.headers, params=self.params, proxies={"http": self.get_proxy()}, timeout=8)
                if response.status_code == 200:
                    html = etree.HTML(response.text)
                    # results = html.xpath("//div[@class='c-border op_fraudphone_container']/div//div[@class='op_fraudphone_word']/strong/text()")

                    results = html.xpath("//div[@class='c-border op_fraudphone_container']/div//div[@class='op_fraudphone_word']")

                    if results:

                        try:
                            mark_person = results[0].xpath("./text()")[0].strip().replace("被", "").replace("个", "")
                        except IndexError:
                            mark_person = "-1"

                        try:
                            tag = results[0].xpath("./strong/text()")[0].replace('"', '')
                        except IndexError:
                            tag = "-1"

                        try:
                            source_site = results[0].xpath("./a/text()")[0]
                        except IndexError:
                            source_site = "-1"

                        print("Parse >>> <{}> <{}> <{}>".format(mark_person, tag, source_site))
                        return mark_person, tag, source_site
                    else:
                        print("empty page >>> <{}> {}".format(number, results))
                        return None
                else:
                    print("状态码异常：{},{},{}\n".format(self.get_now_time(), number, response.status_code))
                    f += 1
            except Exception as e:
                print("请求异常：{},{},{}\n".format(self.get_now_time(), number, e))
                f += 1
        self.add_log("Request value<{}> failed".format(number))
        return None

    def generate_number(self, id_result):
        number_prefix, prefix_id = id_result

        if type(number_prefix) == int:
            number_prefix = str(number_prefix)
        for i in range(10000):
            print(i)
            if self.stop_flag:
                self.redis_conn.sadd(self.redis_db, str(id_result))
                print("循环请求退出， id=<{}>写回redis".format(id_result))
                break
            number_suffix = (4-len(str(i)))*'0'+str(i)
            complete_number = number_prefix + number_suffix
            print("Request >>> {}".format(complete_number))
            req_result = self.req_number(complete_number)
            if req_result:
                mark_person, tag, source_site = self.req_number(complete_number)
                sql = "INSERT INTO number_tag(number,tag,prefix_id,mark_person,source_site) VALUE ('{}','{}','{}','{}','{}')"\
                    .format(complete_number, tag, prefix_id, mark_person, source_site)
                self.mysql_cursor.execute(sql)
                with self.threading_lock:
                    self.mysql_conn.commit()
                print("Insert to MySQL >>> <{}> <{}> <{}> <{}>".format(complete_number, tag, mark_person, source_site))

    def run(self):
        while not self.stop_flag:
            # 获取任务-前缀数据id
            id_result = self.get_task()
            print("Start task >>> prefix&id:{}".format(id_result))
            if id_result:
                # 到mysql查询数据id返回对应的前缀号码
                # print("查询 id {} ".format(id_result))
                # prefix_num = self.search_mysql(id_result)

                # 生成10000个此号码段的请求
                try:
                    self.generate_number(id_result)
                except Exception as e:
                    print("Generate number id=<{}>  raise exception: {}".format(id_result, e))
                    self.add_log("Generate number id=<{}>  raise exception: {}".format(id_result, e))

            else:
                self.add_log("Redis task is empty")
                break
        print("<{}> 线程退出".format(self.threading_name))


if __name__ == '__main__':
    # 连接redis
    print("Connect to redis...")
    r_pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)

    # 连接MySQL
    print("Connect to mysql...")
    m_conn = pymysql.connect(host='192.168.70.40', port=3306, user='root', passwd='mysql', db='phone_number_info', charset='utf8')
    m_cursor = m_conn.cursor()

    # 线程数量
    thread_num = 15
    # 线程锁
    t_lock = threading.Lock()
    # 线程列表
    jobList = []
    try:
        for i in range(thread_num):
            t_name = "Thread-" + str(i+1)
            t = CrawlTelephone(os.getpid(), t_name, m_conn, m_cursor, r_conn, t_lock)
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