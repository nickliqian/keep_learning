import scrapy


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://www.11467.com/zhengzhou/co/244375.htm",
        "http://www.11467.com/qiye/44563472.htm"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        with open(filename+".html", 'wb') as f:
            f.write(response.body)