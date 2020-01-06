import requests
from lxml import etree
import pymysql
import time
import threading
import queue


class CrawlDetail(threading.Thread):
    def __init__(self, m_conn, m_cursor, lock, task_queue, proxies):
        super(CrawlDetail, self).__init__()
        self.m_conn = m_conn
        self.m_cursor = m_cursor
        self.lock = lock
        self.task_queue = task_queue
        self.proxies = proxies
        self.headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            'cache-control': "no-cache",
            'connection': "keep-alive",
            'cookie': "st_si=85648086468091; qgqp_b_id=a4d4fa066eae9f6b7cfd93860f9a6896; emshistory=%5B%22%E6%BC%AB%E6%AD%A5%E8%80%85%22%5D; st_asi=delete; st_pvi=38843502416579; st_sp=2019-12-27%2023%3A29%3A41; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=123; st_psi=20200101162501304-117001300541-1431698992",
            'dnt': "1",
            'host': "guba.eastmoney.com",
            'pragma': "no-cache",
            'referer': "http://guba.eastmoney.com/list,000725_1.html",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }

    def run(self):
        while True:
            r = self.crawl_detail()
            if r:
                pass
            else:
                break
        print("Thread end")
        return None

    # 采集详情页面
    def crawl_detail(self):
        # 按照顺序从数据库获取100个任务
        data = self.get_task()
        if not data:
            return 0

        items = []
        list_ids = []
        for index, d in enumerate(data):
            # 根据之前采集的url构造详细页面url
            list_id, list_url = d

            # 确保采集的是京东方股吧的数据
            if not list_url.startswith("/news,000725"):
                continue

            list_ids.append(list_id)
            url = "http://guba.eastmoney.com{}".format(list_url)
            print("【Request】【{},{}】{}".format(0, index, url))

            while True:
                try:
                    # 采集详情页面
                    # 部分帖子被删除了，访问时由302重定向到404页面，这里禁重定向止被
                    response = requests.request("GET", url, headers=self.headers, timeout=8, proxies=self.proxies,
                                                allow_redirects=False)
                    # 如果发现有302的页面，即说明帖子被删掉了，直接进行下一个任务
                    if response.status_code == 302:
                        print("【Get 404】")
                        with self.lock:
                            with open("404.log", "a+") as f:
                                f.write("{},{},{},{}\n".format(0, index, list_id, list_url))
                        break

                    # 解析页面
                    html = etree.HTML(response.text)
                    elems = html.xpath(
                        "/html/body[@class='hlbody']/div[@class='gbbody ']/div[@id='mainbody']/div[@id='zwcontent']")

                    # 如果页面是空的，说明被反爬了，再次尝试采集
                    if len(elems) == 0:
                        if "<title>429 Too Many Requests</title>" in response.text:
                            raise Exception("429 Too Many Requests")
                        raise Exception("No content")

                    ele = elems[0]

                    item = dict()
                    item["list_id"] = list_id
                    item["用户名"] = extract_data(ele.xpath(".//strong/a/font/text()"))
                    item["用户id"] = extract_data(ele.xpath(".//strong/a/@data-popper"))

                    date_and_client = extract_data(ele.xpath(".//div[@class='zwfbtime']/text()"))
                    item["时间和客户端"] = date_and_client
                    s1 = date_and_client.replace("发表于", "").strip()
                    a, b, c = s1.split(" ")
                    item["发帖时间"] = "{} {}".format(a, b)
                    item["客户端名称"] = c

                    item["标题"] = extract_data(ele.xpath(".//div[@id='zwconttbt']/text()"))

                    item["内容"] = extract_data(ele.xpath(".//div[@id='zwconbody']/div/text()"))
                    if not item["内容"]:
                        item["内容"] = extract_data(ele.xpath(".//div[@id='zwconbody']/div/div/p/text()"))

                    item["来源"] = url
                    print("【Get data】{}:{}".format(item["用户名"], item["标题"]))
                    items.append(item)
                    break
                except Exception as e:
                    print(e)
                    print("request exception, retry...")

                time.sleep(0.01)

        # 将批量完成的任务获得的数据存入数据库
        with self.lock:
            self.insert_detail_data(items, list_ids)
        return 1

    # 用于采集详细页面获取任务列表
    def get_task(self):
        data = []
        for i in range(100):
            if not self.task_queue.empty():
                data.append(self.task_queue.get())
            else:
                break
        return data

    # 将详情页面数据批量存入数据库
    def insert_detail_data(self, items, list_ids):
        # 插入数据
        for item in items:
            sql = "insert into jdf_detail(list_id, 用户名, 用户id, 时间和客户端, 发帖时间, 客户端名称, 标题, 内容, 来源)" \
                  " values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            data = [item["list_id"], item["用户名"], item["用户id"], item["时间和客户端"], item["发帖时间"],
                    item["客户端名称"], item["标题"], item["内容"], item["来源"]]
            self.m_cursor.execute(sql, data)
        print("【Insert 100 rows】")

        # 更新溢已经使用的url
        list_ids_str = str(list_ids).replace("[", "(").replace("]", ")")
        sql = "update jdf set used=1 where id in {}".format(list_ids_str)
        self.m_cursor.execute(sql)
        print("【Update 100 rows】")

        # commit数据
        self.m_conn.commit()


# 根据抽取数据结果返回值
def extract_data(data):
    if len(data) == 0:
        return None
    else:
        return data[0].strip()


# 付费代理服务器
# 防止使用同样的ip地址采集被屏蔽
# 购买地址：https://www.abuyun.com/
def get_proxy():
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H71H5G49VXWDZOQD"
    proxyPass = "2FF6C78E553CDB7A"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }

    return proxies


def make_queue(m_cursor, task_queue):
    offset = 10000
    i = 0
    j = 1
    while True:
        sql = "select id, 链接 from jdf where used=0 limit {},{}".format(i*offset, offset)
        m_cursor.execute(sql)
        data = m_cursor.fetchall()
        i += 1
        for d in data:
            print("\r{} => {}".format(j, d), end="")
            task_queue.put(d)
            j += 1

        if not data:
            print("\nPut queue finished.")
            break


def main():
    # 连接数据库，数据库的基本参数
    mysql_db = "mydata"
    print("Connect to mysql...")
    m_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
    m_cursor = m_conn.cursor()

    # 获取代理地址
    proxies = get_proxy()

    # 队列
    task_queue = queue.Queue(1000000)
    # 任务写入队列
    make_queue(m_cursor, task_queue)

    # 线程锁
    lock = threading.Lock()
    thread_num = 4
    workers = []
    for i in range(thread_num):
        worker = CrawlDetail(m_conn, m_cursor, lock, task_queue, proxies)
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()

    m_cursor.close()
    m_conn.close()
    print("MySQL connection close...")


if __name__ == '__main__':
    main()
