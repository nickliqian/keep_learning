import hashlib
import string
import requests
import re
import time
import os


# 按base64规则解码
def decode_b64str(base64_str):
    base64_charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + '+/'

    # 对每一个base64字符取下标索引，并转换为6为二进制字符串
    base64_bytes = ['{:0>6}'.format(str(bin(base64_charset.index(s))).replace('0b', '')) for s in base64_str if
                    s != '=']
    resp = bytearray()
    nums = len(base64_bytes) // 4
    remain = len(base64_bytes) % 4
    integral_part = base64_bytes[0:4 * nums]

    while integral_part:
        # 取4个6位base64字符，作为3个字节
        tmp_unit = ''.join(integral_part[0:4])
        tmp_unit = [int(tmp_unit[x: x + 8], 2) for x in [0, 8, 16]]
        for i in tmp_unit:
            resp.append(i)
        integral_part = integral_part[4:]

    if remain:
        remain_part = ''.join(base64_bytes[nums * 4:])
        tmp_unit = [int(remain_part[i * 8:(i + 1) * 8], 2) for i in range(remain - 1)]
        for i in tmp_unit:
            resp.append(i)
    # 返回以ASCII码表示的列表
    return resp


# 字符串按md5算法编码
def md5(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()


#
def decode_hash(url_hash, password):
    pswd = password
    pswd = md5(pswd)
    q = 4
    o = md5(pswd[0:16])
    n = md5(pswd[16:])
    l = url_hash[0:4]

    c = o + md5(o+l)

    url_hash = url_hash[4:]
    k = decode_b64str(url_hash)

    h = []
    for g in range(256):
        h.append(g)

    b = []
    for g in range(256):
        i = c[g % len(c)]
        b.append(ord(i))

    f = 0
    for g in range(256):
        f = (f + h[g] + b[g]) % 256
        h[g], h[f] = h[f], h[g]

    t = ""
    k = list(k)

    f = 0
    p = 0
    t = ''
    for g in range(len(k)):
        p = (p + 1) % 256
        f = (f + h[p]) % 256
        h[p], h[f] = h[f], h[p]

        ord1 = k[g]
        ord2 = (h[(h[p] + h[f]) % 256])
        ord3 = ord1 ^ ord2
        t += chr(ord3)
    return t


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/61.0.3163.91 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
}


# 请求html
def get_html(url):
    r = requests.get(url, headers=headers)
    return r.text


# 请求js密码字符串
def get_js_password():
    url = "http://cdn.jandan.net/static/min/1db6c1a9c900052d56757120ca96add6.06100501.js"
    r = requests.get(url, headers=headers)
    pattern = r'\(e,"(.*?)"\);var\sa=\$'
    r_list = re.findall(pattern, r.text)
    password = r_list[0]
    return password


def save_url_list(url):
    password = get_js_password()
    html = get_html(url)
    # 解析目标字符串
    pattern = r'<span\sclass="img-hash">(.*?)</span>'
    url_hash_list = re.findall(pattern, html)

    for url_hash in url_hash_list:
        url_string = decode_hash(url_hash, password)
        url_img = r"http://" + url_string.split(r"//")[1]
        # print("--------------------")
        # print("原始字符串：", url_hash)
        # print("解码字符串：", url_string)
        print("构造url：", url_img)
        down_img(url_img)


def down_img(url):
    r = requests.get(url, headers=headers)
    img_path = 'D://A2//jiandan//' + url[-20:]
    with open(img_path, 'wb') as f:
        f.write(r.content)
    time.sleep(1)

if __name__ == "__main__":
    if not os.path.exists('./jiandanLocation.loc'):
        with open('./jiandanLocation.loc', 'w') as f:
            f.write('0')
            page = 0
    else:
        with open('./jiandanLocation.loc', 'r') as f:
            page = int(f.read())

    for i in range(page, 356):
        try:
            url = 'http://jandan.net/ooxx/page-' + str(i)
            print(">>>", url)
            save_url_list(url)
            time.sleep(10)
        except Exception as e:
            print("第%d页发生问题" % i)
            print("报错:%s" % e)
        finally:
            with open('./jiandanLocation.loc', 'w') as f:
                f.write(str(i))
            break



