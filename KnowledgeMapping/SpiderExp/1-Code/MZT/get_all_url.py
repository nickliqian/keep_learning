import requests
import re
import redis
import hashlib


HEADERS = {
    "Referer": "http://www.mzitu.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
conn_redis = redis.Redis(connection_pool=pool)


def down_img(imgurl):
    response = requests.get(imgurl, headers=HEADERS)
    with open('D:\A\mzt', 'w') as f:
        f.write(response.content)


# 字符串按md5算法编码
def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


# 解析url和存入redis
def parse_html(html):
    # 这个正则用于获取所有内链url
    pattern_all = r'<a.*?href="(.*?mzitu\.com.*?)".*?</a>'
    all_url_list = re.findall(pattern_all, html)
    # 这个正则用于获取图片资源的链接
    pattern_img = r'<a\shref="(http://www.mzitu.com/\d+)"\starget="\_blank">((?!<).*?)</a>'
    img_list = re.findall(pattern_img, html)

    return all_url_list, img_list


def pop_url_check():
    curl = conn_redis.spop('MZT:allURL')
    if curl != None:
        curl = curl.decode('utf-8')
        print(curl)
        pat = r"http://www.mzitu.com/\d+/\d+"
        if re.search(pat, curl) != None:
            return 1
        r = requests.get(curl, headers=HEADERS)
        all_url_list, img_list = parse_html(r.text)

        for value in all_url_list:
            if not conn_redis.sismember('MZT:md5AllURL', md5(value)):
                conn_redis.sadd('MZT:allURL', value)
                conn_redis.sadd('MZT:md5AllURL', md5(value))

        for value in img_list:
            if not conn_redis.sismember('MZT:md5ImgList', md5(value[0])):
                conn_redis.hset('MZT:imgList', value[0], value[1])
                conn_redis.sadd('MZT:md5ImgList', md5(value[0]))
        return 1
    else:
        return 0


def main():
    # 1.访问种子
    surl = 'http://www.mzitu.com/'
    r = requests.get(surl)

    # 2.正则取出所有a标签
    if r.status_code == 200:
        # 初始化
        all_url_list, img_list = parse_html(r.text)
        md5_url_list = list(map(md5, all_url_list))
        # img_list_dict = {i[0]: i[1] for i in img_list}
        # img_list_md5_set = {md5(i[0]) for i in img_list}  # 方法2：dict([(1, 'a'), (3, 'c'), (2, 'b'), (4, 'd')] )
        # 初始储存：分别存md5/url/img到redis
        conn_redis.sadd('MZT:md5AllURL', *md5_url_list)
        conn_redis.sadd('MZT:allURL', *all_url_list)
        for value in img_list:
            if not conn_redis.sismember('MZT:md5ImgList', md5(value[0])):
                conn_redis.hset('MZT:imgList', value[0], value[1])
                conn_redis.sadd('MZT:md5ImgList', md5(value[0]))
    else:
        print('WARNING: status_code != 200')

    # 3. 循环取url获得更多外链
    while True:
        flag = pop_url_check()
        if flag == 0:
            break


if __name__ == "__main__":
    main()