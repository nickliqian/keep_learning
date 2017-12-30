# coding=utf-8
from selenium import webdriver
from lxml import etree


def get_url():
    driver = webdriver.PhantomJS(r"D:\A\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver.get('http://www.tianyancha.com/')
    text = driver.page_source
    with open("./page1.html", "w", encoding="utf-8") as f:
        f.write(text)
    html = etree.HTML(text)
    url = html.xpath("//div[@class='in-block mb10 mr10']/a/@href")
    print(url)
    # area_url = set(url)
    # for each in area_url:
    #     with open("start_url1.py", "a") as f:
    #         f.write('"'+each+'"'+',\n')


def get_headers():
    driver = webdriver.PhantomJS(r"D:\A\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver.get('http://www.httpbin.org/get')
    text = driver.page_source
    with open("./page2.html", "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    get_url()
    # get_headers()