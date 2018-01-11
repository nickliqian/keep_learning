import requests
from lxml import etree
import time
import redis
import os


# 全局变量
POOL = redis.ConnectionPool(host='127.0.0.1', port=6379)
CONN_REDIS = redis.Redis(connection_pool=POOL)

LIST_URL = "http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxr&detail=true&sxbzxrmc=&proselect" \
           "=&cityselect=&disselect="

HEADERS_JUST_UA = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62"
                  " Safari/537.36"
}


class CrawlError(Exception):
    pass


class OprateFileError(Exception):
    pass


def oprate_file(filename, mode, content="r"):
    if not (isinstance(filename, str) & isinstance(filename, str) & isinstance(filename, str)):
        raise TypeError("filename, mode, content 应该是str类型的值")

    # 如果没有文件就在当前路径新建一个
    if not os.path.exists(filename):
        with open(filename, "w") as f:
            pass
    # 判断读写模式
    if mode == "w":
        with open(filename, "w") as f:
            f.write(content)
    elif mode == "r":
        with open(filename, "r") as f:
            value =  f.read()
            return value
    elif mode == "a":
        with open(filename, "a") as f:
            f.write(content)
    else:
        raise OprateFileError("暂不支持 '%s' 操作模式" % mode)


def crawl_page(num):
    s = time.time()
    print("正在采集第%d页" % num)
    while True:
        try:
            response = requests.post(url=LIST_URL, data={'curPageNO': str(num)}, headers=HEADERS_JUST_UA, timeout=10)
            if response.text == "":
                raise CrawlError
            break
        except Exception:
            print("重试请求--")
            time.sleep(1)
            pass

    if response.status_code == 200:

        # 保证html dom可用
        try:
            html = etree.HTML(response.text)
            name_list = html.xpath("//table//tr//td/a/text()")
        except Exception as e:
            print("xpath解析出错")
            oprate_file("xpath解析出错.html", "w", response.text)
            raise e

        # 保证内容完整
        if len(name_list) != 10:
            raise CrawlError("name_list数量不足10个")

        for name in name_list:
            name = name.strip()
            print(name, end=" ")
            CONN_REDIS.sadd("NameFromHLJ", name)
    else:
        oprate_file("response响应不是200.html", "w", response.text)
        raise CrawlError("响应不是200")

    e = time.time()
    print(" >> 消耗时间：", float("%.5f" % (e-s)))


def main():
    record_filename = "hlj_record.loc"
    if not os.path.exists(record_filename):
        oprate_file(record_filename, "w", "1")

    # 读取记录
    start = oprate_file(record_filename, "r")

    for i in range(int(start), 100001):
        try:
            crawl_page(i)
            time.sleep(3)
        except KeyboardInterrupt:
            print("记录位置", i)
            oprate_file(record_filename, "w", str(i))
            print("手动终止")
            break
        except Exception as e:
            print("记录位置", i)
            oprate_file(record_filename, "w", str(i))
            print("出错了...")
            raise e


if __name__ == '__main__':
    main()
