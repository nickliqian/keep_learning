import json
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
from json.decoder import JSONDecodeError
from requests.exceptions import ReadTimeout, ConnectionError


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
        self.domain = "http://www.11467.com"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 "
                          "(KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
        }
        self.params = {
            "f": "h5",
            "page": "1",
        }

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
                # self.logger.debug("proxy: {}".format(ip_num))
                return ip_num
            except Exception as get_proxy_error:
                # self.logger.debug(get_proxy_error)
                time.sleep(1)

    # check response, means site refuse get normal page, need repeat request
    def check_response_abnormal(self, response):
        if "too many request" in response.text:
            return True
        else:
            return False

    # request special url
    def req_url(self, target_url, page_num):
        time.sleep(1)
        self.params["page"] = str(page_num)
        while not self.stop_flag:
            try:
                response = requests.get(url=target_url, headers=self.headers, params=self.params,
                                        proxies={"http": self.get_proxy_from_wuyou_api()}, timeout=8)
                if response.status_code == 404:
                    return None
                elif response.status_code == 200:
                    if self.check_response_abnormal(response):
                        pass
                    else:
                        return response
                else:
                    self.logger.warning(
                        "response status code abnormal <{}> <{}>".format(target_url, response.status_code))
            except Exception as request_error:
                if isinstance(request_error, ReadTimeout):
                    pass
                elif isinstance(request_error, ConnectionError):
                    pass
                else:
                    self.logger.debug("request abnormal <{}> <{}> <{}>".format(type(request_error), target_url, request_error))
                # raise request_error

    # parse html or json data
    def parse_page(self, task_dict):
        page_num = 1
        while not self.stop_flag:
            self.logger.debug("Crawl >>> {}?f=h5&page={}".format(task_dict['street_url'], page_num))
            response = self.req_url(task_dict['street_url'], page_num)
            if not response:
                raise ResponseAbnormalError()
            if response.text != "[]":
                data = json.loads(response.text)
                res_bool = data["resBool"]

                if not res_bool:
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

                        sql = "insert into soufang_price(house_id, name, provinceId, cityId, cityAreaId, subwayStation," \
                              " spiderSource, address, rentCount, saleCount, buildPriceAvg, buildPriceAvgUnit," \
                              " salesStatusPeriods, priceDate, source_href, city_name, area_name, street_name)" \
                              " VALUE ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}'," \
                              "'{}','{}')".format(house_id, name, provinceId, cityId, cityAreaId, subwayStation,
                                                  spiderSource, address, rentCount, saleCount, buildPriceAvg,
                                                  buildPriceAvgUnit, salesStatusPeriods, price_data, response.url,
                                                  task_dict["city_name"], task_dict["city_name"], task_dict["city_name"])
                        with self.threading_lock:
                            m_cursor.execute(sql)
                            m_conn.commit()

                    page_num += 1
                else:
                    break
            else:
                break

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
            task = self.get_task()
            # start schedule task
            try:
                if task:
                    self.logger.debug("Task >>> {}".format(task))
                    self.parse_page(task)
                else:
                    self.logger.info("Redis has no task")
                    self.redis_empty_callback()
            # if any exception, rollback task to redis
            except Exception as main_error:
                self.logger.debug("Rollback >>> {}".format(task))
                self.redis_conn.sadd(self.redis_key, task)

                # for ResponseAbnormalError, just re-request
                if isinstance(main_error, ResponseAbnormalError):
                    pass
                else:
                    self.logger.error("Response exception >>> {} >>> {}".format(task, main_error))
                    # raise main_error

        self.logger.debug("Threading quit")


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
    # logger.debug("Test logging debug")
    # logger.info("Test logging info")
    # logger.warning("Test logging warning")

    return logger


if __name__ == '__main__':

    db_dict = {
        # redis
        "redis_host": "127.0.0.1",
        "redis_port": 6379,
        "redis_key": "soufang:task",
        # mysql
        "mysql_host": "192.168.70.40",
        "mysql_port": 3306,
        "mysql_user": "root",
        "mysql_password": "mysql",
        "mysql_db": "soufang",
        "mysql_table": "soufang_price",
        # other config
        "thread_count": 5,
        "project_name": "spider.com.soufang",
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
        time.sleep(25)
        m_cursor.close()
        m_conn.close()
        print("进程 {} 已经退出".format(os.getpid()))
