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


# 根据抽取数据结果返回值
def extract_data(data):
    if len(data) == 0:
        return None
    else:
        return data[0].strip()


def crawl():
    # 获取代理地址（使用代理IP可以防止本机IP被对方的网站屏蔽）
    proxies = get_proxy()
    # 链接地址（书评数据的地址，通过传递不同的参数采集每一页的数据）
    url = "https://book.douban.com/subject/3155622/comments/new"
    # 请求头（没有请求头爬虫可能会被对方屏蔽）
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
    # 如果记录页数的文件不存在，说明是第一次采集，则创建初始化文件
    if not os.path.exists("start.txt"):
        with open("start.txt", "w+") as f:  # 创建start.txt文件
            f.write("1")                    # 在文件中写入数字1

    # 读取记录页数的文件，获得当前采集的页数
    with open("start.txt", "r") as f:
        page_num = int(f.read())

    # 循环的翻页，每次翻页成功后 page_num+1，如果程序中断则把当前的page_num写到文件start.txt中去
    while True:
        # 翻页参数，通过抓包获得，修改page_num的参数值，可以采集不同页码的数据
        querystring = {"p": str(page_num)}
        # 请求网页数据
        # 这里是循环的作用：如果采集成功则break退出，否则再次尝试采集
        while True:
            try:
                print("Crawl page {}".format(page_num))
                # 向采集链接发送请求，如果正常请求则不会报错，break退出到下一步
                response = requests.request("GET", url, headers=headers, params=querystring, proxies=proxies, timeout=8)
                break
            except Exception as e:
                # 抛出异常说明超时或者访问被禁止、代理不可用、没有网络等情况，会再次请求数据
                print("请求失败，重试中...{}".format(e))

        # 如果请求代码不是200，显式抛出错误
        # 显式抛出是为了提醒这里是未知的情况，需要人工判断改异常的出现原因，修正爬虫逻辑
        if not response.status_code == 200:
            raise Exception("请求异常")

        # 请求到数据后，我们发现数据是json格式，主要内容在content里面
        # 通过 response.json()["content"] 提取我们需要的数据
        html_data = response.json()["content"]
        # 提取到和评论有关的html后，进行页面数据解析
        html = etree.HTML(html_data)
        # 通过xpath定位所有的条目
        elems = html.xpath("//li")

        # 这是最后一页的标志
        # 如果页面没有数据，说明到了最后一页，跳出循环
        if not elems:
            print("Finished!")
            break

        # 解析具体数据
        # 新建列表用于储存此页中每一条评论数据
        items = []
        for elem in elems:
            # 创建一个字段用于储存每条评论的相关数据字段
            item = dict()
            # 提取投票赞同的字段
            item["vote"] = extract_data(elem.xpath(".//span[@class='comment-vote']/span/text()"))
            # 提取用户名称字段
            item["user"] = extract_data(elem.xpath(".//span[@class='comment-info']/a/text()"))
            # 提取用户链接字段
            item["user_url"] = extract_data(elem.xpath(".//span[@class='comment-info']/a/@href"))

            # 提取评分等级字段
            star_string = extract_data(elem.xpath(".//span[@class='comment-info']/span/@class"))
            # 评分等级字段信息需要通过正则表达式提取出来
            if star_string:
                item["star"] = re.findall(r".*?allstar(\d+).*?", star_string)[0]
            else:
                item["star"] = None

            # 提取评分等级对应的程度词
            item["level"] = extract_data(elem.xpath(".//span[@class='comment-info']/span/@title"))
            # 提取评论的时间
            item["release_time"] = extract_data(elem.xpath(".//span[@class='comment-info']/span[2]/text()"))
            # 提取评论内容
            item["content"] = extract_data(elem.xpath(".//p[@class='comment-content']/span/text()"))

            # 将一条评论加入到列表中
            items.append(item)

        # 将本页的评论数据追加到csv文件中
        # 存数据到csv文件
        with open("data.csv", "a+", newline='', encoding="utf-8") as f:
            # 定义表头
            fieldnames = ['vote', 'user', 'user_url', 'star', 'level', 'release_time', 'content']
            # 定义CSV对象用于写入数据
            f_csv = csv.DictWriter(f, fieldnames=fieldnames)

            # 第一页额外写入表头
            if page_num == 1:  # 这里判断是否是第一页采集
                f_csv.writeheader()

            # 批量写入数据
            # 写入每一页的10个评论数据
            f_csv.writerows(items)

        # 页码加一，用于下一次采集
        print("Write {} rows data to csv".format(len(items)))
        page_num += 1

        # 写入记录页数的文件
        # 防止中断程序后，重复进行采集，将当前的采集进度持久化储存在文件中
        with open("start.txt", "w") as f:
            f.write(str(page_num))

        # 设置时间间隔
        # 1. 是避免程序太快的进行循环大量占用CPU
        # 2. 是避免采集频率过快IP被屏蔽
        time.sleep(0.05)


def main():
    crawl()


if __name__ == '__main__':
    main()
