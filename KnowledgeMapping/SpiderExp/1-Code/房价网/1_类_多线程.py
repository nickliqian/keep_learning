import os
import re
import pymysql
import requests
from lxml import etree
import time
import random
import redis
import threading
import logging
import json
from constant import city2code_dict


class ResponseAbnormalError(Exception):
    pass


class SpiderMySQLRedis(threading.Thread):
    def __init__(self, mysql_conn, mysql_cursor, redis_conn, threading_lock, mysql_table, redis_key, logger):
        super(SpiderMySQLRedis, self).__init__()
        # 项目参数

        self.logger = logger

        # 进程线程参数
        self.threading_lock = threading_lock
        self.stop_flag = False

        # 数据库连接
        # MySQl
        self.mysql_conn = mysql_conn
        self.mysql_cursor = mysql_cursor
        self.mysql_table = mysql_table
        # Redis
        self.redis_conn = redis_conn
        self.redis_key = redis_key

        # 网络请求参数
        self.domain = "http://{}.fangjia.com/trend/year2Data"
        self.querystring = {
            "defaultCityName": "北京",
            "districtName": "",
            "region": "",
            "block": "",
            "keyword": "巷上嘉园"
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/65.0.3325.181 Safari/537.36"}

    @staticmethod
    def timestamp2date(timestamp):
        return time.strftime("%Y%m%d", time.localtime(timestamp))

    # 获取redis任务
    def get_task(self):
        info_byte = self.redis_conn.spop(self.redis_key)
        if info_byte:
            info = info_byte.decode("utf-8")
            info_dict = eval(info)
            return info_dict
        else:
            return None

    # get proxy from redis wuyou api
    def get_proxy_from_wuyou_api(self):
        while True:
            try:
                num_list = [k_i for k_i in range(1, 21)]
                ip_choice = random.choice(num_list)
                ip_str = "myip" + str(ip_choice)
                ip_num = self.redis_conn.mget(ip_str)[0]
                if not ip_num:
                    return None
                ip_num = ip_num.decode('utf-8')
                self.logger.debug("proxy: {}".format(ip_num))
                return ip_num
            except Exception as get_proxy_error:
                self.logger.debug(get_proxy_error)
                time.sleep(1)

    # check response, means site refuse get normal page, need repeat request
    def check_response_abnormal(self, response):
        pass

    # request special url
    def req_url(self, default_city_name, keyword, url_code):
        # 参数拼接
        target_url = self.domain.format(url_code)
        self.querystring["defaultCityName"] = default_city_name
        self.querystring["keyword"] = keyword

        # 请求
        f = 0
        while f < 8:
            try:
                response = requests.get(url=target_url,
                                        headers=self.headers,
                                        params=self.querystring,
                                        proxies={"http": self.get_proxy_from_wuyou_api()},
                                        timeout=8)
                if response.status_code == 404:
                    return None

                if response.text == "null":
                    self.logger.warning("未查询到此数据 <{}> <{}> <{}>".format(default_city_name, keyword, target_url))
                    return None

                if response.status_code == 200:
                    if self.check_response_abnormal(response):
                        raise ResponseAbnormalError
                    return response

                else:
                    self.logger.warning(
                        "response status code abnormal <{}> <{}>".format(target_url, response.status_code))
                    f += 1
            except Exception as request_error:
                self.logger.debug("request abnormal <{}> <{}>".format(target_url, request_error))
                f += 1
        self.logger.error("Request failed for five times <{}>".format(target_url))
        return None

    # parse html or json data
    def parse_page(self, response, default_city_name, keyword, url_code):

        content = json.loads(response.text)

        real_house_name = content["series"][0]["name"]
        price_list = content["series"][0]["data"]
        for stamp_price in price_list:
            item = []
            evaluation_time = self.timestamp2date(stamp_price[0]/1000)
            price = stamp_price[1]
            item = [default_city_name, real_house_name, evaluation_time, price]
            # self.logger.debug("{}  {}  {}  {}元/平米".format(default_city_name, real_house_name, evaluation_time, price))

            with self.threading_lock:
                self.save_data(item)
        self.logger.warning("正在保存数据 <{}> <{}> <{}>".format(default_city_name, keyword, self.domain.format(url_code)))

    # insert data to db or file
    def save_data(self, item):
        sql = "INSERT INTO fangjia (city, houses_name, time_point, price) VALUE ('{}','{}','{}','{}')".format(*item)
        self.mysql_cursor.execute(sql)
        self.mysql_conn.commit()

    # stop threading
    def stop(self):
        self.logger.debug("stop_flag(停止标志) = True")
        self.stop_flag = True

    def redis_empty_callback(self):
        self.stop()

    # start
    def run(self):
        while not self.stop_flag:

            # get task num/dict/data
            # {'code': 'cq', 'city': '重庆', 'house': '南山明珠'}
            task = self.get_task()

            # start schedule task
            try:
                if task:
                    self.logger.debug("Start task <{}>".format(task))
                    default_city_name, keyword, url_code = task["city"], task["house"], task["code"]

                    response = self.req_url(default_city_name, keyword, url_code)
                    if response:
                        self.parse_page(response, default_city_name, keyword, url_code)
                    time.sleep(0.5)

                else:
                    self.logger.info("Redis has no task")
                    self.redis_empty_callback()
            # if any exception, rollback task to redis
            except Exception as main_error:
                self.redis_conn.sadd("lianjia_task_error", task)
                # for ResponseAbnormalError, just re-request
                if isinstance(main_error, ResponseAbnormalError):
                    pass
                else:
                    self.logger.error("Task <{}> response exception as <{}>".format(task, main_error))
                    # self.stop()
                    # raise main_error

        self.logger.info("Threading quit")


# register logger
def register_logger(project_name):
    # 初始化组件
    logger = logging.getLogger(project_name)
    logger.setLevel(level=logging.DEBUG)

    # 公共格式
    file_formatter = logging.Formatter(
        '%(asctime)s - %(process)d - %(thread)d - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 输出到文件的初始化
    log_file = logging.FileHandler("./log.txt")
    log_file.setLevel(level=logging.INFO)
    log_file.setFormatter(file_formatter)

    # 输出到控制台的初始化
    log_console = logging.StreamHandler()
    log_console.setLevel(level=logging.DEBUG)
    log_console.setFormatter(console_formatter)

    # 注册
    logger.addHandler(log_file)
    logger.addHandler(log_console)

    # 测试
    logger.debug("Test logging debug")
    logger.info("Test logging info")
    logger.warning("Test logging warning")

    return logger


if __name__ == '__main__':

    db_dict = {
        # redis
        "redis_host": "127.0.0.1",
        "redis_port": 6379,
        "redis_key": "fangjiawang_task",
        # mysql
        "mysql_host": "192.168.70.40",
        "mysql_port": 3306,
        "mysql_user": "root",
        "mysql_password": "mysql",
        "mysql_db": "fangjiawang",
        "mysql_table": "fangjia",
        # other config
        "thread_count": 5,
        "project_name": "spider.com.fangjiawang",
    }

    # 注册记录器
    project_logger = register_logger(db_dict["project_name"])

    # 连接redis
    print("Connect to redis...")
    r_pool = redis.ConnectionPool(host=db_dict["redis_host"], port=db_dict["redis_port"])
    r_conn = redis.Redis(connection_pool=r_pool)

    # 连接MySQL
    print("Connect to mysql...")
    m_conn = pymysql.connect(host=db_dict["mysql_host"], port=db_dict["mysql_port"], user=db_dict["mysql_user"],
                             passwd=db_dict["mysql_password"], db=db_dict["mysql_db"], charset='utf8')
    m_cursor = m_conn.cursor()

    # 线程配置
    thread_num = db_dict["thread_count"]
    t_lock = threading.Lock()
    jobList = []
    try:
        for i in range(thread_num):
            t = SpiderMySQLRedis(m_conn,
                                 m_cursor,
                                 r_conn,
                                 t_lock,
                                 db_dict["mysql_table"],
                                 db_dict["redis_key"],
                                 project_logger)
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
