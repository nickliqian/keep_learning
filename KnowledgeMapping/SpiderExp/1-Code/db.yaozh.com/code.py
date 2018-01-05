import requests
from lxml import etree


def test(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"}

    r = requests.get(url, headers=headers)
    html = etree.HTML(r.text)

    trs = html.xpath('//div[@class="table-wrapper"]/table//tr')

    item = {}
    print('--------------------------------')
    for tr in trs:
        th = tr.xpath('.//th/text()')[0].strip()
        td = tr.xpath('.//span/text()')[0].strip()
        print(th, td)
        item[th] = td
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    print(item)
    print('--------------------------------')


if __name__ == "__main__":
    url1 = "https://db.yaozh.com/hmap/21.html"
    url2 = "https://db.yaozh.com/hmap/22.html"
    test(url1)
    test(url2)