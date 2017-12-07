from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from lxml import etree
import requests
import re


def get_links(who_sells=0):
    # urls = []
    list_view = 'http://bj.58.com/pbdn/{}/'.format(str(who_sells))
    print(list_view)
    wb_data = requests.get(list_view, headers=headers)
    # print(wb_data.text)
    # soup = BeautifulSoup(web_data.text, 'lxml')
    p = r'<a\sonClick="clickLog\(\'from=zzpc_infoclick\'\);"\shref="(.*?)"\starget="_blank">'
    links = re.findall(p, wb_data.text)
    # links = soup.select('td.t')
    print(1, links)


def get_info(url):
    try:
        if web_data.status_code == 200:
            title = soup.title.text
            # print(title)
            price = soup.select('#content span.price')
            date = soup.select('li.time')
            # print(date)
            area = soup.select('span.c_25d')
            # print(list(area[0].stripped_strings))
            data = {
                'title': title,
                'price': price[0].text,
                'date': date[0].text,
                'area': list(area[0].stripped_strings),
                'cate': None,
                'views': None
            }
            print(11, data)
    except RequestException:
        pass


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

url = 'http://bj.58.com/pingbandiannao/30223879694911x.shtml'
web_data = requests.get(url, headers=headers)
# print(web_data.text)
soup = BeautifulSoup(web_data.text, 'lxml')

get_info(url)
get_links(0)

'''
#infolist > div.left > a.title.t

'''
