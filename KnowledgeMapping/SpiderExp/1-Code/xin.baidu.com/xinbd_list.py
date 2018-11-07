# -*- coding: utf-8 -*-
# @Topic : 
# @Title : 
# @Content : 
# @Author : LiQian
# @Create Time : 2018/11/07 11:20
# @Update Time : 2018/11/07 11:20
import requests
from lxml import etree
import re
import execjs


class ParseError(Exception):
    pass


def req_list(company_key_word):
    # 请求list
    url = "https://xin.baidu.com/s?q=%E6%97%A0%E9%94%A1%E5%B0%8F%E5%A4%A9%E9%B9%85&t=0"
    params = {
        "q": company_key_word
    }
    response = sess.get(url=url, headers=headers, timeout=8, params=params)

    html = etree.HTML(response.text)
    elements = html.xpath("//div[@class='zx-ent-info']/div[@class='zx-ent-items']/h3[@class='zx-ent-title']/a[@class='zx-list-item-url']")

    # 保存list所有结果
    items = []
    for ele in elements:
        item = dict()
        item["name"] = ele.xpath("./@title")[0]
        item["href"] = ele.xpath("./@href")[0]
        print(item)
        items.append(item)
    return items


def req_detail(pid):
    # 请求detail
    url = "https://xin.baidu.com/detail/compinfo?pid={}".format(pid)
    print("请求 {}".format(url))
    response = sess.get(url=url, headers=headers, timeout=8)

    # 保存页面
    with open("html.html", "w") as f:
        f.write(response.text)
    return response.text


def parse_detail(content):
    # 解析页面
    html = etree.HTML(content)

    # 真实pid
    pid_pre = re.findall(r',"result":{"pid":"(.*?)","defTags":', content)
    if pid_pre:
        pid = pid_pre[0]
    else:
        raise ParseError("无法获得公司的pid")

    # 百度信用代码
    baiducode_pre = html.xpath("//span[@id='baiducode']/text()")
    if baiducode_pre:
        baiducode = baiducode_pre[0]
    else:
        raise ParseError("无法获得公司的百度信用代码baiducode")

    # mix函数代码
    mix_code_pre = html.xpath("//script[4]/text()")
    if mix_code_pre:
        mix_code = mix_code_pre[0]
    else:
        raise ParseError("无法获得mix_code脚本")

    # tk元素id和属性
    tk_kw_pre = re.findall(r"document\.getElementById\('(.*?)'\)\.getAttribute\('(.*?)'\)", mix_code)
    if tk_kw_pre and len(tk_kw_pre[0]) == 2:
        tk_kw = tk_kw_pre[0]
        tk_id = tk_kw[0]
        tk_attr = tk_kw[1].lower()
        print("id:{} attr:{}".format(tk_id, tk_attr))
    else:
        raise ParseError("无法获得tk相关id和属性的值")

    # 构造xpath解析指定的tk参数
    xpath_code = "//*[@id='{}']/@{}".format(tk_id, tk_attr)
    tk = html.xpath(xpath_code)
    if tk:
        tk = tk[0]
    else:
        raise ParseError("无法获得根据tk参数获取指定的tk值")

    print("tk:{} bid:{}".format(tk, baiducode))
    mix_js = mix_code.split("(function(){var tk")[0]
    ctx = execjs.compile(mix_js)
    tot = ctx.call("mix", tk, baiducode)
    print("tot: {}".format(tot))

    return pid, tot


def req_base_info(pid, tot):
    url = "https://xin.baidu.com/detail/basicAjax"
    params = {
        "pid": pid,
        "tot": tot
    }
    response = sess.get(url=url, headers=headers, params=params, timeout=8)

    print(response.text)


def main():
    global headers
    global sess
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
    }
    # 创建会话
    sess = requests.session()
    # 请求列表
    key_word = "无锡小天鹅股份有限公司"
    items = req_list(key_word)
    pid = items[0]["href"].replace("/detail/compinfo?pid=", "")
    # 请求详细页面
    content = req_detail(pid)
    # 解析请求参数
    pid, tot = parse_detail(content)
    req_base_info(pid, tot)


if __name__ == '__main__':
    main()
