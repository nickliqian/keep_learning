import requests
from lxml import etree
import time
import re


def req_url(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
    f = 0
    while f < 3:
        try:
            response = requests.get(url=url, headers=headers, timeout=8)
            text = response.text
            if response.status_code == 200:
                if (text.startswith("采集大神饶命")) or ("too many request" in text) or "":
                    time.sleep(1)
                    print("error")

                if text.startswith("没找到"):
                    print("页面没有数据：没找到 {}".format(url))

                parse_page(response)
                break
            else:
                print("状态码异常")
                f += 1
        except Exception as e:
            print("请求异常：{},{}\n".format(type(e), e))
            f += 1


def parse_page(response):
    html = etree.HTML(response.text)

    # 抽取公司名称
    results = html.xpath("//div[@class='f_l']/h4/a")
    print("本次抓取公司名称<{}>个".format(len(results)))
    if results:
        for result in results:
            name = result.xpath("./text()")[0].strip()
            href = result.xpath("./@href")[0].strip("//")
            # print(name, href)
    else:
        flag = re.findall(r"(没有找到相关公司)", response.text)
        if flag:
            print("本分类无公司")
            return 0
        else:
            print("出现了一点异常")

    # 判断是否有下一页
    results = html.xpath("//div[@class='pages']/a/em/../following-sibling::*[1]")
    if results:
        result = results[0]
        flag = result.xpath("./text()")[0]
        print("下一个标签是 <{}>".format(flag))
        if flag != "尾页":
            href = result.xpath("./@href")[0].strip("//")
            if not href.startswith("http://"):
                href = "http://" + href
            req_url(href)
        else:
            print("已经是最后一页")
    else:
        print("本分类仅一页")


if __name__ == '__main__':
    url = "http://wulanchabu.11467.com/fengzhen/pn9399"
    req_url(url)
