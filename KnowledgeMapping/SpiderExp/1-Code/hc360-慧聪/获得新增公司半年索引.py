import requests
import json
from lxml import etree
import time
import redis
import random


year_list = [{'tag': '2018.01-2018.06', 'href': 'http://b2b.hc360.com/xingongsi/2018s.html'},
             {'tag': '2017.07-2017.12', 'href': 'http://b2b.hc360.com/xingongsi/2017f.html'},
             {'tag': '2017.01-2017.06', 'href': 'http://b2b.hc360.com/xingongsi/2017s.html'},
             {'tag': '2016.07-2016.12', 'href': 'http://b2b.hc360.com/xingongsi/2016f.html'},
             {'tag': '2016.01-2016.06', 'href': 'http://b2b.hc360.com/xingongsi/2016s.html'},
             {'tag': '2015.07-2015.12', 'href': 'http://b2b.hc360.com/xingongsi/2015f.html'},
             {'tag': '2015.01-2015.06', 'href': 'http://b2b.hc360.com/xingongsi/2015s.html'},
             {'tag': '2014.07-2014.12', 'href': 'http://b2b.hc360.com/xingongsi/2014f.html'},
             {'tag': '2014.01-2014.06', 'href': 'http://b2b.hc360.com/xingongsi/2014s.html'},
             {'tag': '2013.07-2013.12', 'href': 'http://b2b.hc360.com/xingongsi/2013f.html'},
             {'tag': '2013.01-2013.06', 'href': 'http://b2b.hc360.com/xingongsi/2013s.html'}]


# 从redis获取代理IP
def get_proxy():
    while True:
        try:
            num_list = [i for i in range(1, 21)]
            ip_choice = random.choice(num_list)
            ip_str = "myip" + str(ip_choice)
            ip_num = r_conn.mget(ip_str)[0]
            if not ip_num:
                return None
            ip_num = ip_num.decode('utf-8')
            # print("proxy: %s" % ip_num)
            return ip_num
        except Exception as e:
            print(e)
            time.sleep(1)


def get_one_index():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    url = "https://b2b.hc360.com/xingongsi/2018f.html"
    response = requests.get(url, headers=headers)

    html = etree.HTML(response.text)

    results = html.xpath("//div[@class='left fl']/div[@class='left2_con']/ul[@class='industry_word']/li/a")

    items = []
    for r in results:
        item = {}
        item['tag'] = r.xpath("./text()")[0].strip().replace("新增公司", "")
        item['href'] = r.xpath("./@href")[0]
        items.append(item)
    print(items)


def get_day_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    response = requests.get(url, headers=headers)

    html = etree.HTML(response.text)

    results = html.xpath("//div[@class='left fl']/div[@class='left2_con']/ul[@class='industry_word']/li/a")

    items = []
    for r in results:
        item = {}
        item['tag'] = r.xpath("./text()")[0].strip().replace("新增公司", "")
        if "." in item['tag']:
            continue
        item['href'] = r.xpath("./@href")[0]
        items.append(item)
        print(item)
    return items


def write_day_url():
    task_items = []
    for u in year_list:
        task = get_day_url(u['href'])
        for t in task:
            task_items.append(t)
    print(task_items)
    with open("./task_items.json", "w") as f:
        data = json.dumps(task_items, ensure_ascii=False)
        f.write(data)


def get_day_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }

    # 采集指定URL
    while True:
        try:
            response = requests.get(url, headers=headers, proxies={"http": get_proxy(), "https": get_proxy()}, timeout=6)
            print("status_code: {}".format(response.status_code))
            if response.status_code in (200, 404):
                break
        except Exception:
            pass

    html = etree.HTML(response.text)
    results = html.xpath("/html/body/div[@class='main']/div[4]/div[@class='left fl']/div[@class='bk']/ul[@class='r_list']/li/a")
    print("解析结果数为：", len(results))
    if len(results) == 0:
        empty_flag = html.xpath("/html/body/div[@class='main']/div[4]/div[@class='left fl']/h2[@class='null']/text()")
        if empty_flag:
            if empty_flag[0].strip() == "暂无任何公司信息……":
                print("页面信息为空")
            else:
                raise TypeError("页面为空 -> 报错")

    for r in results:
        try:
            name = r.xpath("./text()")[0]
        except IndexError:
            continue
        href = r.xpath("./@href")[0]
        # print(name, href)
        with open("./data.csv", "a+") as fd:
            fd.write("{},{}\n".format(name, href))

    # 判断是否存在下一页
    next_flag = html.xpath("//div[@class='page_mod']/span[@class='page_next']/a[@class='page_next']/@href")
    if next_flag:
        print("开始下一页")
        get_day_data(next_flag[0])


def crawl_all():

    with open("./task_items.json", "r") as f:
        content = json.load(f)
        total = len(content)

    i = 1
    for c in content:
        if i > 27:
            print("{}/{} {}".format(i, total, c))
            get_day_data(c["href"])
        i += 1


if __name__ == '__main__':
    # 连接redis
    print("Connect to redis...")
    r_pool = redis.ConnectionPool(host='192.168.70.40', port=6379)
    r_conn = redis.Redis(connection_pool=r_pool)
    crawl_all()
    # get_day_data("https://b2b.hc360.com/xingongsi/20180608.html")