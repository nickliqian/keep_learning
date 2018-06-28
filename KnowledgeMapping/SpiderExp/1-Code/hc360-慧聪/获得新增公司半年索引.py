import requests
from lxml import etree

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


def get_day_url():
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    url = "http://b2b.hc360.com/xingongsi/2018s.html"
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
    print(items)


if __name__ == '__main__':
    get_day_url()