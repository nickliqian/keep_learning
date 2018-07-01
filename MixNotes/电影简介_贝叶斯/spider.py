import requests
from lxml import etree


def get_page(num):
    url = "https://movie.douban.com/top250?start={}&filter=".format(num)
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    hrefs = html.xpath("//div[@class='article']/ol[@class='grid_view']/li/div[@class='item']/div[@class='info']/div[@class='hd']/a/@href")
    for h in hrefs:
        print(h)
        with open("./hrefs.txt", "a+") as f:
            f.write("{}\n".format(h))


def save_hrefs_to_txt():
    for i in range(10):
        print("第{}页".format(i))
        get_page(i*25)


def crawl_desc():
    pass


if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }


