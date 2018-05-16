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


class CrawlInterrupterError(Exception):
    pass


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
        self.url = "http://www.baidu.com/s"
        self.params = {"wd": "1388888888"}
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}

    # 返回标准时间
    @staticmethod
    def get_now_time():
        time_obj = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return str(time_obj)

    # 停止运行
    def stop(self):
        print("停止标志 >>> stop_flag = True")
        self.stop_flag = True

    # 向公共log文件中添加log信息
    def add_log(self, desc):
        with self.threading_lock:
            with open("./crawl.log", "a+") as f:
                f.write("<{}> desc:<{}>\n".format(self.get_now_time(), desc))

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
        while True:
            try:
                num_list = [i for i in range(1, 21)]
                ip_choice = random.choice(num_list)
                ip_str = "myip" + str(ip_choice)
                ip_num = self.redis_conn.mget(ip_str)[0]
                if not ip_num:
                    return None
                ip_num = ip_num.decode('utf-8')
                # print("proxy >>> {}".format(ip_num))
                return ip_num
            except Exception as get_proxy_error:
                print("get proxy error >>> {}".format(get_proxy_error))
                time.sleep(1)

    def req_number(self, number, id_result):
        self.params["wd"] = number
        while True:
            # 判断线程状态
            if self.stop_flag:
                self.redis_conn.sadd(self.redis_db, str(id_result))
                print("循环请求退出 >>> id<{}>写回redis".format(id_result))
                break
            try:
                response = requests.get(url=self.url, headers=self.headers, params=self.params,
                                        proxies={"http": self.get_proxy()},
                                        timeout=8, verify=True)
                if response.status_code == 200:
                    html = etree.HTML(response.text)
                    results = html.xpath("//div[@class='c-border op_fraudphone_container']/div//div[@class='op_fraudphone_word']")

                    # 判断xpath结果是否为空，不为空则进一步解析并返回数据，否则返回None
                    if results:
                        # 如果解析不到某个字段就置为-1
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

                        return mark_person, tag, source_site
                    else:
                        return None
                else:
                    self.add_log("状态码异常 >>> {},{},{}".format(self.get_now_time(), number, response.status_code))
            except Exception as req_number_e:
                # 连接过程中异常
                if isinstance(req_number_e, requests.ConnectionError):
                    print("requests.ConnectionError")
                elif isinstance(req_number_e, requests.ReadTimeout):
                    print("requests.ReadTimeout")
                else:
                    print("请求异常 >>> {},{},{},{}".format(self.get_now_time(), number, type(req_number_e), req_number_e))

    def generate_number(self, id_result):
        # 初始化请求参数 >>> number_prefix:号码前缀 prefix_id:前缀对应表中的id
        number_prefix, prefix_id = id_result
        if type(number_prefix) == int:
            number_prefix = str(number_prefix)

        # 开始循环10000
        for tail_num in range(10000):

            # 判断线程状态
            if self.stop_flag:
                self.redis_conn.sadd(self.redis_db, str(id_result))
                print("循环请求退出 >>> id<{}>写回redis".format(id_result))
                break
            # 组合号码并请求
            number_suffix = (4-len(str(tail_num)))*'0'+str(tail_num)
            complete_number = number_prefix + number_suffix
            try:
                print("Request >>> {}".format(complete_number))
                req_result = self.req_number(complete_number, id_result)
                # 判断请求结果 tuple->(save to mysql) or None->(pass)
                if req_result:
                    mark_person, tag, source_site = req_result
                    # 插入数据库
                    sql = "INSERT INTO number_tag(number,tag,prefix_id,mark_person,source_site) VALUE ('{}','{}','{}','{}','{}')"\
                        .format(complete_number, tag, prefix_id, mark_person, source_site)
                    with self.threading_lock:
                        self.mysql_cursor.execute(sql)
                        self.mysql_conn.commit()
                    print("{} Insert to MySQL >>> <{}> <{}> <{}> <{}>".format(self.get_now_time(), complete_number, tag, mark_person, source_site))
            except Exception as generate_number_error:
                print("Generate_number error >>> {}".format(complete_number))
                self.add_log("Generate_number error >>> {},{},{}".format(type(complete_number), complete_number, generate_number_error))
                # raise generate_number_error

    def run(self):
        while not self.stop_flag:
            # 获取任务-前缀数据id
            id_result = self.get_task()
            # print("Start task >>> prefix&id:{}".format(id_result))
            if id_result:

                # 生成10000个此号码段的请求
                try:
                    self.generate_number(id_result)
                except Exception as run_error:
                    raise run_error
            else:
                print("Redis task is empty >>> break")
                break
        print("<{}> threading quit".format(self.threading_name))


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
    except KeyboardInterrupt:
        # 手动停止时,执行所有对象的stop函数
        if jobList:
            for t in jobList:
                t.stop()
    except Exception as main_error:
        # info_by_mail(">> gd spider stop", "进程报错 >> {}: {}".format(type(e), e))
        raise main_error
    finally:
        m_cursor.close()
        m_conn.close()
        time.sleep(25)
        print("进程 {} 已经退出".format(os.getpid()))