import requests
from lxml import etree
import time
import os


file_dir = r"D:\A\blog_img"


def crawl(url):
    response = requests.get(url=url)
    response.encoding = "GBK"

    html = etree.HTML(response.text)
    urls = html.xpath("//table/tr/td/table/tbody/tr/td/table/tr[1]/td/div/a/@href")

    for url in urls:
        print(url)

        response = requests.get(url=url)
        response.encoding = "GBK"
        html = etree.HTML(response.text)
        try:
            down_url = html.xpath("//div[@class='down']/a[2]/@href")[0]
            img_name = html.xpath("//div[@class='PhotoDiv']/h2/text()")[0]
        except Exception as e:
            print(e)
            continue

        print(down_url)
        print(img_name)

        time.sleep(2)

        response = requests.get(url=down_url)

        file_name = os.path.join(file_dir, img_name + ".rar")

        with open(file_name, "wb") as f:
            f.write(response.content)

        time.sleep(2)


if __name__ == '__main__':
    root_url_a = "http://so.sccnn.com/search/%E9%A3%8E%E6%99%AF/"
    root_url_b = ".html"

    for i in range(150):
        root_url = root_url_a + str(i) + root_url_b
        crawl(root_url)

