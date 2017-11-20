from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
import time
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

def get_info(url):
    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        print(response.text)
        if response.status_code == 200:
            # return response.text
            soup = BeautifulSoup(response.text, 'lxml')
            titles = soup.select('div.pho_info > h4')
            addresses = soup.select('span.pr5')
            prices = soup.select('#pricePart > div.day_1 > span')
            images = soup.select('#floatRightBox > div.js_box.clearfix > div.w_pic > a > img')
            names = soup.select('#floatRightBox > div.js_box.clearfix > div.w_240 > h6 > a')
            sexes = soup.select('#floatRightBox > div.js_box.clearfix > div.member_pic > div')
            for title, address, price, image, name, sex in zip(titles, addresses, prices, images, names, sexes):
                data = {
                    'title': title.get_text().strip(),
                    'address': address.get_text().strip(),
                    'price': price.get_text(),
                    'image': image.get('src'),
                    'name': name.get_text().strip(),
                    'sex': sex.get('class')
                }
                print(data)

        return None
    except RequestException:
        return None

def main(url):
    get_info(url)

if __name__ == '__main__':
    # urls = ['https://bj.xiaozhu.com/search-duanzufang-p{}-0'.format(number) for number in range(1, 14)]
    urls = ['https://bj.xiaozhu.com/search-duanzufang-p{}-0/'.format(number) for number in range(1, 14)]
    # main(url)
    for single_url in urls:
        print(single_url)
        main(single_url)


















