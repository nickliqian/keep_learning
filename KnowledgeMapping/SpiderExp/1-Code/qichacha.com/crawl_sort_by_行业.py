import json
import requests
from lxml import etree
import time


def get_big_sort():
    url = "http://www.qichacha.com/industry_A.html"
    # 参数设置
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    site = "http://www.qichacha.com"
    response = requests.get(url=url, headers=headers)

    html = etree.HTML(response.text)

    results = html.xpath("/html/body/div[@class='container m-t-md']/div[@class='row']/div[@class='col-md-12'][1]/div[@class='panel b-a padder'][1]/dl[@class='filter-tag clearfix']/dd/a")

    items = []
    for r in results:
        item = []
        content = {}
        name = r.xpath("./text()")[0].strip()
        href = r.xpath("./@href")[0].strip()
        content["sort_big"] = name
        content["sort_small"] = "全局"
        content["href"] = site + href
        item.append(content)
        items.append(item)
    print(items)


def get_small_sort(big_sort_url, big_sort_name, number):
    # 参数设置
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
    }
    site = "http://www.qichacha.com"
    response = requests.get(url=big_sort_url, headers=headers)

    html = etree.HTML(response.text)

    results = html.xpath("/html/body/div[@class='container m-t-md']/div[@class='row']/div[@class='col-md-12'][1]/div[@class='panel b-a padder'][2]/dl[@class='filter-tag clearfix']/dd/a")

    for r in results:
        content = {}
        name = r.xpath("./text()")[0].strip()
        href = r.xpath("./@href")[0].strip()
        content["sort_big"] = big_sort_name
        content["sort_small"] = name
        content["href"] = site + href
        ITEMS[i].append(content)
        print(big_sort_name, name, site + href)


if __name__ == '__main__':
    with open("./行业分类1.json", "r") as f:
        rs = f.read()
    ITEMS = json.loads(rs)
    back = ITEMS
    for i in range(len(back)):
        this_url = back[i][0]["href"]
        this_big_sort_name = back[i][0]["sort_big"]
        print(this_url)
        get_small_sort(this_url, this_big_sort_name, i)
        time.sleep(2)
    print(ITEMS)
    with open("./行业分类2.json", "w") as f:
        text = json.dumps(ITEMS, ensure_ascii=False)
        f.write(text)

"""
[
    [
        {'href': 'http://www.qichacha.com/industry_A.html', 'sort_big': '农、林、牧、渔业', 'sort_small': '全局'},
        {'href': 'http://www.qichacha.com/industry_A.html', 'sort_big': '农、林、牧、渔业', 'sort_small': '全局'},
        {'href': 'http://www.qichacha.com/industry_A.html', 'sort_big': '农、林、牧、渔业', 'sort_small': '全局'},
        ...
    ],
    [
        {'href': 'http://www.qichacha.com/industry_A.html', 'sort_big': '农、林、牧、渔业', 'sort_small': '全局'},
        {'href': 'http://www.qichacha.com/industry_A.html', 'sort_big': '农、林、牧、渔业', 'sort_small': '全局'},
        {'href': 'http://www.qichacha.com/industry_A.html', 'sort_big': '农、林、牧、渔业', 'sort_small': '全局'},
        ...
    ],
    ...
]

"""
