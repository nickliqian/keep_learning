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
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/65.0.3325.181 Safari/537.36"}

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
    def req_url(self, target_url):
        time.sleep(1)
        f = 0
        while f < 8:
            try:
                response = requests.get(url=target_url, headers=self.headers,
                                        proxies={"http": self.get_proxy_from_wuyou_api()}, timeout=8)
                if response.status_code == 404:
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
    def parse_page(self, street_url, origin, task_dict):
        print("\nCrawl >>> " + street_url)
        response = self.req_url(street_url)
        if response:
            html = etree.HTML(response.text)

            count = html.xpath(
                "/html/body/div[@class='content']/div[@class='leftContent']/div[@class='resultDes clear']"
                "/h2[@class='total fl']/span/text()")[0]

            print(">>> 本街道共有小区{}个".format(count))

            if int(count) == 0:
                return None

            results = html.xpath("/html/body/div[@class='content']/div[@class='leftContent']/ul[@class='listContent']"
                                 "/li[@class='clear xiaoquListItem']")

            print("---------------本页的小区为---------------")
            for result in results:
                # 小区名称
                builing_name = result.xpath("./div[@class='info']/div[@class='title']/a/text()")[0]
                builing_name = pymysql.escape_string(builing_name)
                # 小区详情页面链接
                builing_href = result.xpath("./div[@class='info']/div[@class='title']/a/@href")[0]
                # 小区信息
                house_info = result.xpath("./div[@class='info']/div[@class='houseInfo']/a")
                house_type_count = None
                if len(house_info) == 3:
                    house_type_count = house_info[0].xpath("./text()")[0]
                    house_type_count = re.findall(r"共(\d+)个", house_type_count)[0]

                # 30天内成交套数
                house_buy = house_info[-2].xpath("./text()")[0]
                house_buy = re.findall(r"成交(\d+)套", house_buy)[0]

                # 正在出租的数量
                house_rent = house_info[-1].xpath("./text()")[0]
                house_rent = re.findall(r"(\d+)套正在出租", house_rent)[0]

                house_feature = result.xpath("./div[@class='info']/div[@class='positionInfo']/a")
                house_district = house_feature[0].xpath("./text()")[0]
                house_bizcircle = house_feature[1].xpath("./text()")[0]

                house_type = result.xpath("./div[@class='info']/div[@class='positionInfo']/text()")

                try:
                    house_type_string = house_type[3].replace("\xa0", "").replace("\n", "").replace(" ", "").strip("/")
                    year = house_type_string.split("/")[-1]
                    year = re.findall(r"(.*?)年建成", year)[0]
                except IndexError:
                    house_type_string = "None"
                    year = "None"

                price_data = time.strftime("%Y%m%d")

                # 价格
                price = result.xpath(".//div[@class='totalPrice']/span/text()")[0].strip()
                price_desc = result.xpath(".//div[@class='priceDesc']/text()")[0].strip()

                item = [price_data, builing_name, builing_href, house_type_count, house_buy, house_rent, house_district,
                        house_bizcircle, year, house_type_string, task_dict["city_name"], task_dict["area_name"],
                        task_dict["street"], task_dict["href"], price, price_desc]

                self.logger.debug(str(item))

                with self.threading_lock:
                    self.save_data(item)

            if int(count) > 30:
                try:
                    j_next = html.xpath("//div[@class='page-box house-lst-page-box']/@page-data")[0]
                    cur_page = int(eval(j_next)["curPage"])
                    total_page = int(eval(j_next)["totalPage"])
                    print(">>> 本页是第{}页，共有{}页".format(cur_page, total_page))
                    if cur_page == total_page:
                        print(">>> 本街道已经采集完成")
                        return None
                    else:
                        pg = "pg" + str(cur_page + 1) + "/"
                        return origin + pg
                except Exception as check_next_page_error:
                    raise check_next_page_error
            else:
                print(">>> 无下一页")

    # insert data to db or file
    def save_data(self, item):
        sql = "INSERT INTO {}(price_data,builing_name,builing_href,house_type_count,house_buy,house_rent,house_district,house_bizcircle,year,house_type_string,city_name,area_name,street,source_href,price,price_desc) VALUE ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')" \
            .format(self.mysql_table, *item)
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
            task = self.get_task()

            # start schedule task
            try:
                if task:
                    self.logger.debug("Start task <{}>".format(task))

                    url = task["href"]
                    origin = url
                    while True:
                        if url:
                            url = self.parse_page(url, origin, task)
                        else:
                            break
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
        "redis_key": "lianjia_list_task",
        # mysql
        "mysql_host": "192.168.70.40",
        "mysql_port": 3306,
        "mysql_user": "root",
        "mysql_password": "mysql",
        "mysql_db": "lianjia",
        "mysql_table": "lianjia_price",
        # other config
        "thread_count": 3,
        "project_name": "spider.com.lianjia",
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
