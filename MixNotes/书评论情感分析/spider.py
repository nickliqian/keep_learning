import requests
from lxml import etree
import re
import os
import csv
import time


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

    return proxies


# 根据抽取数据结果返回值
def extract_data(data):
    if len(data) == 0:
        return None
    else:
        return data[0].strip()


def crawl():
    proxies = get_proxy()
    # 链接地址
    url = "https://book.douban.com/subject/3155622/comments/new"
    # 请求头
    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        'cache-control': "no-cache",
        'connection': "keep-alive",
        'dnt': "1",
        'host': "book.douban.com",
        'pragma': "no-cache",
        'referer': "https://book.douban.com/subject/3155622/comments/hot?p=2",
        'sec-fetch-mode': "cors",
        'sec-fetch-site': "same-origin",
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
        'x-requested-with': "XMLHttpRequest",
        }

    # 判断是否存在记录页数的文件
    if not os.path.exists("start.txt"):
        with open("start.txt", "w+") as f:
            f.write("1")

    # 读取记录页数的文件
    with open("start.txt", "r") as f:
        page_num = int(f.read())

    while True:
        # 翻页参数
        querystring = {"p": str(page_num)}
        # 请求网页数据
        while True:
            try:
                print("Crawl page {}".format(page_num))
                response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxies, timeout=8)
                break
            except Exception as e:
                print("请求失败，重试中...{}".format(e))

        # 如果请求代码不是200，显式抛出错误
        if not response.status_code == 200:
            raise Exception("请求异常")

        # 页面数据解析
        html_data = response.json()["content"]
        html = etree.HTML(html_data)
        elems = html.xpath("//li")

        # 如果页面没有数据，说明到了最后一页，跳出循环
        if not elems:
            print("Finished!")
            break

        # 解析具体数据
        items = []
        for elem in elems:
            item = dict()
            item["vote"] = extract_data(elem.xpath(".//span[@class='comment-vote']/span/text()"))
            item["user"] = extract_data(elem.xpath(".//span[@class='comment-info']/a/text()"))
            item["user_url"] = extract_data(elem.xpath(".//span[@class='comment-info']/a/@href"))

            star_string = extract_data(elem.xpath(".//span[@class='comment-info']/span/@class"))
            if star_string:
                item["star"] = re.findall(r".*?allstar(\d+).*?", star_string)[0]
            else:
                item["star"] = None

            item["level"] = extract_data(elem.xpath(".//span[@class='comment-info']/span/@title"))
            item["release_time"] = extract_data(elem.xpath(".//span[@class='comment-info']/span[2]/text()"))
            item["content"] = extract_data(elem.xpath(".//p[@class='comment-content']/span/text()"))
            items.append(item)

        # 存数据到csv文件
        with open("data.csv", "a+", newline='', encoding="utf-8") as f:
            fieldnames = ['vote', 'user', 'user_url', 'star', 'level', 'release_time', 'content']
            f_csv = csv.DictWriter(f, fieldnames=fieldnames)

            # 第一页额外写入表头
            if page_num == 1:
                f_csv.writeheader()

            # 批量写入数据
            f_csv.writerows(items)

        # 页码加一
        print("Write {} rows data to csv".format(len(items)))
        page_num += 1

        # 写入记录页数的文件
        with open("start.txt", "w") as f:
            f.write(str(page_num))

        time.sleep(0.05)


def main():
    crawl()


if __name__ == '__main__':
    main()
