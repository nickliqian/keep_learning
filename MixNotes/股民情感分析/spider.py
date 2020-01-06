import requests
from lxml import etree
import pymysql
import time
import threading


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
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }

    proxies = {
        "http": "http://213.234.238.52:8080",
        "https": "https://213.234.238.52:8080",
    }

    return proxies


# 根据抽取数据结果返回值
def extract_data(data):
    if len(data) == 0:
        return None
    else:
        return data[0].strip()


# 将列表页面采集的数据存入mysql
def insert_list_data(m_cursor, m_conn, items):
    for item in items:
        sql = "insert into jdf(阅读, 评论, 标题, 链接, 作者, 最后更新帖子时间, 来源) values (%s,%s,%s,%s,%s,%s,%s)"
        data = [item["阅读"], item["评论"], item["标题"], item["链接"], item["作者"], item["最后更新帖子时间"], item["来源"]]
        m_cursor.execute(sql, data)
        m_conn.commit()


# 爬取列表页面的帖子数据
def crawl_list(m_conn, m_cursor, proxies):
    # 请求头
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'cache-control': "no-cache",
        'connection': "keep-alive",
        'cookie': "st_si=85648086468091; qgqp_b_id=a4d4fa066eae9f6b7cfd93860f9a6896; emshistory=%5B%22%E6%BC%AB%E6%AD%A5%E8%80%85%22%5D; st_pvi=38843502416579; st_sp=2019-12-27%2023%3A29%3A41; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=20; st_psi=20191228120041303-117001301474-0931182961; st_asi=delete",
        'dnt': "1",
        'host': "guba.eastmoney.com",
        'pragma': "no-cache",
        'referer': "http://guba.eastmoney.com/list,000725.html",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    }

    # 获取爬取页面的记录
    with open("start.txt", "r") as f:
        start_num = int(f.read())

    try:
        # 循环翻页爬取
        for i in range(start_num, 8582):
            # 构造url
            url = "http://guba.eastmoney.com/list,000725_{}.html".format(i)
            print("【Crawl】{}".format(url))

            while True:
                try:
                    # 发出请求
                    response = requests.request("GET", url, headers=headers, timeout=10, proxies=proxies)
                    # 解析数据
                    html = etree.HTML(response.text)
                    elems = html.xpath(
                        "/html/body[@class='hlbody']/div[@class='gbbody'][5]/div[@id='mainbody']/div[@id='articlelistnew']/div")

                    items = []
                    for ele in elems:
                        item = dict()
                        item["阅读"] = extract_data(ele.xpath("./span[1]/text()"))
                        item["评论"] = extract_data(ele.xpath("./span[2]/text()"))
                        item["标题"] = extract_data(ele.xpath("./span[3]/a/text()"))
                        item["链接"] = extract_data(ele.xpath("./span[3]/a/@href"))
                        item["作者"] = extract_data(ele.xpath("./span[4]/a/font/text()"))
                        item["最后更新帖子时间"] = extract_data(ele.xpath("./span[5]/text()"))
                        item["来源"] = url
                        if item["链接"] == None:
                            pass
                        elif item["链接"].startswith("http"):
                            pass
                        else:
                            items.append(item)

                    # 正常会获取70~100条数据，如果获取到的数据过少说明被反爬了，抛出错误后重试
                    if len(items) < 3:
                        raise Exception("no 11 rows")

                    break
                except Exception as e:
                    print(e)
                    print("request exception, retry...")

            # 将一页的数据批量存入数据库
            insert_list_data(m_cursor, m_conn, items)

            # 保存任务进度，防止意外退出后需要重新采集
            start_num += 1
            with open("start.txt", "w") as f:
                f.write(str(start_num))

            print("【Get】rows {}".format(len(items)))

            # 降低采集频率，防止被屏蔽和重试时消耗计算机性能
            time.sleep(0.2)
    finally:
        m_cursor.close()
        m_conn.close()
        print("MySQL connection close...")


# 用于采集详细页面获取任务列表
def get_task(loop_batch, commit_batch_count, m_cursor):
    sql = "select id, 链接 from jdf limit {},{}".format(loop_batch*100, commit_batch_count)
    print(sql)
    m_cursor.execute(sql)
    data = m_cursor.fetchall()
    return data


# 将详情页面数据批量存入数据库
def insert_detail_data(m_cursor, m_conn, items):

    for item in items:
        sql = "insert into jdf_detail(list_id, 用户名, 用户id, 时间和客户端, 发帖时间, 客户端名称, 标题, 内容, 来源)" \
              " values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        data = [item["list_id"], item["用户名"], item["用户id"], item["时间和客户端"], item["发帖时间"],
                item["客户端名称"], item["标题"], item["内容"], item["来源"]]
        m_cursor.execute(sql, data)
        m_conn.commit()


# 采集详情页面
def crawl_detail(m_conn, m_cursor, proxies):
    headers = {
        'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        'accept-encoding': "gzip, deflate",
        'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'cache-control': "no-cache",
        'connection': "keep-alive",
        'cookie': "st_si=85648086468091; qgqp_b_id=a4d4fa066eae9f6b7cfd93860f9a6896; emshistory=%5B%22%E6%BC%AB%E6%AD%A5%E8%80%85%22%5D; st_asi=delete; _adsame_fullscreen_18009=1; st_pvi=38843502416579; st_sp=2019-12-27%2023%3A29%3A41; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=89; st_psi=20191229110446106-117001300541-4211861707",
        'dnt': "1",
        'host': "guba.eastmoney.com",
        'pragma': "no-cache",
        'referer': "http://guba.eastmoney.com/list,000725_1.html",
        'upgrade-insecure-requests': "1",
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    }

    # 定义从mysql获取任务的参数
    commit_batch_count = 100  # 每次获取的任务数量（同时也是批量存入数据库的数据条数）
    list_count = 685938  # 总共的任务数量
    loop_count = int(list_count / commit_batch_count) + 1  # 需要批量存入的轮数

    # 获取任务进度
    with open("start_detail.txt", "r") as f:
        start_num = int(f.read())

    # 循环获取任务并采集详情页面，批量存入数据库
    for loop_batch in range(start_num, loop_count):

        # 按照顺序从数据库获取100个任务
        data = get_task(loop_batch, commit_batch_count, m_cursor)

        items = []
        for index, d in enumerate(data):
            # 根据之前采集的url构造详细页面url
            list_id, list_url = d
            url = "http://guba.eastmoney.com{}".format(list_url)
            print("【Crawl】【{},{}】{}".format(loop_batch, index, url))

            while True:
                try:
                    # 采集详情页面
                    # 部分帖子被删除了，访问时由302重定向到404页面，这里禁重定向止被
                    response = requests.request("GET", url, headers=headers, timeout=10, proxies=proxies, allow_redirects=False)
                    # 如果发现有302的页面，即说明帖子被删掉了，直接进行下一个任务
                    if response.status_code == 302:
                        print("【Get 404】")
                        with open("404.log", "a+") as f:
                            f.write("{},{},{},{}\n".format(loop_batch, index, list_id, list_url))
                        break

                    # 解析页面
                    html = etree.HTML(response.text)
                    elems = html.xpath("/html/body[@class='hlbody']/div[@class='gbbody ']/div[@id='mainbody']/div[@id='zwcontent']")

                    # 如果页面是空的，说明被反爬了，再次尝试采集
                    if len(elems) == 0:
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

        # 将批量完成的任务获得的数据存入数据库
        insert_detail_data(m_cursor, m_conn, items)

        # 保存任务进度
        start_num += 1
        with open("start_detail.txt", "w") as f:
            f.write(str(start_num))


# 启动函数
def main():
    # 连接数据库，数据库的基本参数
    mysql_db = "mydata"
    print("Connect to mysql...")
    m_conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='mysql', db=mysql_db, charset='utf8')
    m_cursor = m_conn.cursor()

    # 获取代理地址
    proxies = get_proxy()

    # 采集列表
    crawl_list(m_conn, m_cursor, proxies)

    # 采集详情
    # crawl_detail(m_conn, m_cursor, proxies)


if __name__ == '__main__':
    main()
