import requests
import redis
from lxml import etree
import hashlib
import os
import time

HEADERS = {
    "Referer": "http://www.mzitu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}
with open('./log_error.txt', 'w') as f:
    f.write(str(time.time()) + '\n')
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
conn_redis = redis.Redis(connection_pool=pool)


# 字符串按md5算法编码
def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


# 生成key值的set，这里用不上
def get_all_key():
    lis = conn_redis.hkeys("MZT:imgList")
    conn_redis.sadd("MZT:keyImgList", *lis)


def log_error(string):
    with open('./log_error.txt', 'a') as f:
        f.write(string + "\n")


# 获得一个url和item名称
def pop_item():
    key_url = conn_redis.spop("MZT:keyImgList")
    if key_url:
        value_name = conn_redis.hget("MZT:imgList", key_url)
        return key_url.decode('utf-8'), value_name.decode('utf-8')
    else:
        return 0, 0


def request_get_url(url, headers):
    i = 1
    while i<=3:
        try:
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200:
                return response
        except Exception as e:
            print("Request url fail: %s \n url is %s .Retry %d!" % (e, url, i))
            i += 1


# 获取页码
def parse_html(img_page_url):
    response = request_get_url(img_page_url, HEADERS)
    try:
        html = etree.HTML(response.text)
        img_page_href = html.xpath('//div[@class="pagenavi"]/a[last()-1]/@href')[0]
        page_num = img_page_href.split(r'/')[-1]
        page_num = int(page_num)
        print('page_num is', page_num)
        return page_num
    except Exception as e:
        raise Exception("Can't get this <page num>:", e, img_page_url)


# 根据每一页的url获取每一页图片的url
def parse_img_url(url):
    response = request_get_url(url, HEADERS)
    print("Requests thr url: ", url)
    try:
        html = etree.HTML(response.text)
        img_src = html.xpath("//div[@class='main-image']/p/a/img/@src")[0]
        return img_src
    except Exception as e:
        raise Exception("Can't get this page <img src>:", e, url)


def down_img(imgurl, file_path):
    response = request_get_url(imgurl, HEADERS)
    try:
        file = imgurl.replace('http://i.meizitu.net', '').replace('/', '')
        file_name = os.path.join(file_path, file)
        print("Save file to --> %s" % file)
        with open(file_name, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        raise Exception("Can't <download img>:", e, imgurl)


def get_item_img():
    key_url, value_name = pop_item()
    if key_url == 0:
        return 0
    print("Start catch %s" % key_url)
    try:
        # 获取页码和构造文件储存路径
        page_num = parse_html(key_url)
        root_path = "D:\A\mzt"
        file_path = os.path.join(root_path, value_name + '-' + str(page_num) + 'P')
        if not os.path.exists(file_path):
            os.mkdir(file_path)

        # 下载对应的图片
        for i in range(page_num):
            img_page_url = key_url + '/' + str(i+1)
            img_url = parse_img_url(img_page_url)
            down_img(img_url, file_path)

    except Exception as e:
        conn_redis.sadd("MZT:ErrorKeyImgList", key_url)
        print("!!!!!!Had Error:", e)
        log_error(key_url + " -> " + str(e))
    return 1


if __name__ == "__main__":
    i = 1
    s = 0
    e = 0
    while True:
        if i == 1:
            s = time.time()
        flag = get_item_img()
        i += 1
        # 每下载10次休息
        if i == 10:
            e = time.time()
            t = e - s
            print("策略性的休息中...上10组耗时为%d秒" % t)
            conn_redis.rpush("MZT:SpendTime", t)
            rest_num = conn_redis.scard("MZT:keyImgList")
            rest_time = float(int(rest_num)/10 * t)/60
            print("剩余%s组，预计耗时%.2f分钟(约%.2f小时)" % (rest_num, rest_time, rest_time/60))
            time.sleep(60)
            i = 1
        # 没有任务的标志
        if flag == 0:
            print("Already download all images!")
            break
    # 恢复所有下载信息
    # get_all_key()
