# -*- coding:utf-8 _*-
import sys
import re
import urllib2
import random
from aip import AipOcr
from urllib import urlretrieve
from PIL import Image
import xlwt
import time

ua = ["Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1",
      "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0",
      "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
      'Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.0 Safari/534.13',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/533.3 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/533.3',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.8 (KHTML, like Gecko) Chrome/7.0.521.0 Safari/534.8',
      'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.458.1 Safari/534.3',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.66 Safari/535.11',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.8 (KHTML, like Gecko) Chrome/17.0.940.0 Safari/535.8',
      'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.77 Safari/535.7ad-imcjapan-syosyaman-xkgi3lqg03!wgz'
      ]


# 将png的透明背景色变成白色
def background_turn_white(image_name):
    """ 将png的透明背景色变成白色 """
    im = Image.open(image_name)
    x, y = im.size

    # 使用白色来填充背景
    p = Image.new('RGBA', im.size, (255, 255, 255))
    p.paste(im, (0, 0, x, y), im)
    white_picture_name = 'white' + image_name
    p.save(white_picture_name)
    return white_picture_name


# 获取图片
def get_picture(page, image_url):
    """ 获取图片 """
    picture_name = str(page) + 'ziroom.png'
    urlretrieve(url=image_url, filename=picture_name)
    return picture_name


# 读取图片
def get_file_content(file_path):
    """ 读取图片 """
    with open(file_path, 'rb') as fp:
        return fp.read()


# 利用百度ocr将图片转成文字
def bai_du_ocr(white_picture_name):
    """ 你的 APPID AK SK """
    # APP_ID = '**'
    # API_KEY = '**'
    # SECRET_KEY = '**'
    image = get_file_content(white_picture_name)

    import urllib, urllib2, sys
    import json
    import ssl
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=oHQBGNLCEsBP411EvWkQoDAY&client_secret=CUr1wuDWSfsHNIR223NFpPNrva7Byj04'
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        print(content)

    # APP_ID = '15340698'
    # API_KEY = 'oHQBGNLCEsBP411EvWkQoDAY'
    # SECRET_KEY = 'CUr1wuDWSfsHNIR223NFpPNrva7Byj04'

    # client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


    """ 调用通用文字识别（高精度版） """
    # client.basicAccurate(image)
    # options j= {}
    """ 带参数调用通用文字识别（高精度版） """
    # price_res = client.basicAccurate(image, options)

    # return price_res['words_result'][0]['words']


# 当ocr少识别一个数字的时候挽救一波
# 挽救不了，位置不确定
def find_lost_number(price_string):
    list_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    for num in range(0, 9):
        list_num.remove(int(price_string[num]))

    return list_num[0]


# 将文字转成对应的价格
def get_ziroom_price(page, ROOM_PRICE):
    ROOM_PRICE = eval(ROOM_PRICE)
    image_url = 'http:' + ROOM_PRICE['image']
    print(image_url)
    offsets = ROOM_PRICE['offset']
    picture_name = get_picture(page, image_url)  # 将图片下载到本地
    white_picture_name = background_turn_white(picture_name)  # 将下载的图片背景色改成白色
    price_string = bai_du_ocr(white_picture_name)  # 解析出图片的文字

    if len(price_string) == 10:
        prices = []
        # 遍历offset，取出对应的价格
        for offset in offsets:
            if len(offset) == 4:
                price = price_string[offset[0]] + price_string[offset[1]] + price_string[offset[2]] + price_string[
                    offset[3]]
            else:
                price = 0
            prices.append(price)
            # print(prices)
        return prices
    else:
        print(('百度OCR识别有问题：' + image_url))
        return [0 for i in range(0, len(offsets))]


# 解析页面
def parse_html(url):
    '''
    :param url:  请求的网址
    :return: 解析出的结果页面
    '''
    req = urllib2.Request(url)
    req.add_header('User-Agent', random.choice(ua))
    open = urllib2.build_opener()
    html_source = open.open(req).read()
    return html_source


# 存到excel中
def save_excel(data):
    workbook = xlwt.Workbook(encoding='utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok=True)

    for i, row in enumerate(data):
        for j, col in enumerate(row):
            booksheet.write(i, j, col)
    workbook.save('ziroom.xls')


if __name__ == '__main__':

    # 获取当前的url有多少页
    # http://www.ziroom.com/z/nl/d23008624-b611100364-z3.html
    get_url_page = 'http://www.ziroom.com/z/nl/d23008624-b611100364-z3.html'
    get_url_page_pat = '下一页</a>.*?<span>共(.*?)页</span>'
    pages_html = parse_html(get_url_page)
    pages = re.compile(get_url_page_pat, re.S).findall(pages_html)[0]
    # print(pages)
    #
    # data = []  # 存储爬下来的数据
    page= 2
    # for page in range(1, int(pages) + 1):

    url = get_url_page + 'p=' + str(page)
    room_name_pat = 'class="t1">(.*?)</a>'
    # <a target="_blank" href="(.*?)" class="t1">

    room_url_pat = '<a target="_blank" href="(.*?)" class="t1">.*?</a>'
    room_local_pat = '<h4><a target="_blank" href=".*?">(.*?)</a></h4>'
    room_detail_pat = '<div class="detail">.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?<span>(.*?)</span>.*?</p>'
    room_distance_pat = '<p><span>(.*?)</span></p>'
    room_price_pat = 'var ROOM_PRICE = (.*?);'
    #
    f = parse_html(url)  # 解析页面获得页面的源代码

    room_name = re.compile(room_name_pat, re.S).findall(f)  # 名称
    room_url = re.compile(room_url_pat, re.S).findall(f)  # 链接
    room_local = re.compile(room_local_pat, re.S).findall(f)  # 位置
    room_detail = re.compile(room_detail_pat, re.S).findall(f)  # 详细
    room_distance = re.compile(room_distance_pat, re.S).findall(f)  # 地铁的距离
    room_prices_list = re.compile(room_price_pat, re.S).findall(f)  # 价格的image和offset
    # print(room_url)
    room_square_meters = []
    room_floors = []
    room_bedrooms = []
    # print(room_url)
    # print('----')
    # print(room_name)
    # print(room_local)
    # print(room_detail)
    # print(room_distance)
    # room_prices_list = room_prices_list[0]
    # print(room_prices_list)
    for room_prices in room_prices_list:

        room_price = get_ziroom_price(page, room_prices)
        print(room_price)
    # print(room_name)
    # for k in range(0, len(room_name)):
    #     room_square_meters.append(room_detail[k][0])  # 平方米
    #     room_floors.append(room_detail[k][1])  # 楼层
    #     room_bedrooms.append(room_detail[k][2])  # 几居室
    #     print(room_square_meters + room_floors+room_bedrooms)
        # for i in range(0, len(room_price)):
        #     data.append((str(page) + '-' + str(i + 1), room_name[i], room_url[i], room_local[i], room_distance[i],
        #                  room_square_meters[i], room_floors[i], room_bedrooms[i], room_price[i]))

        # time.sleep(3)  # 百度OCR的调用太频繁容易失败
    # save_excel(data)
