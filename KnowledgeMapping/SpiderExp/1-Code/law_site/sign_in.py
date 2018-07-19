#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
from lxml import etree
import time
import re


def get_csrf_value():
    # success
    # 获取csrf参数
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }
    login_form_url = "http://openlaw.cn/login.jsp"
    response = sess.request("GET", url=login_form_url, headers=headers)
    # print(response.cookies.items())
    html = etree.HTML(response.text)
    csrf_value = html.xpath("//input[@name='_csrf']/@value")[0]
    print("csrf_value -> {}".format(csrf_value))
    return csrf_value


def get_verify_value():
    # 获取验证码
    v = str(time.time()).replace(".", "")[:-4]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }
    url = "http://openlaw.cn/Kaptcha.jpg?v={}".format(v)
    response = sess.get(url=url, headers=headers)
    with open("./p.png", "wb") as f:
        f.write(response.content)
    # 输入验证码
    verify_value = str(input("Input validate code:"))
    return verify_value



def login():
    pwd = "FjOUpfGaybqaFkeZH7YFqOhhQPOprUJCoKQ/v7hbfe6AplyztqTV95oa9zwkz2rHoXL4aUXL/678GOa8bidaIaAMCnYAs39/YkVIQKcvJYZC3u" \
          "IP3Q4bhnhi8SnVm6S6R2n4QnDNANjgKE0G6zKhdHnL29JHihY+nQb08UtKwvvF3motJoK/nmZpQg1cvS1TlIzicknyXMHMF9W5d4VT6XQf3Qb8" \
          "SZUFyBcnlbuHNnYBBn3i1s7fqGWDTPMDjeJDKEKEvEWcPTF2v8y+jurvpT41Bw/hrNX3jh2ix833j98GyeMJxZnllAuMiZktTJNha+N9tnEfOg" \
          "aTMqXp1pw+eg==:::Cm2S60BdWt+KQGMvrX7P6w=="
    sign_in_url = "http://openlaw.cn/login"
    data = {
        "_csrf": csrf_value,
        "username": "aciyz2pa@dawin.com",
        "password": pwd,
        "code": verify_value,
        "_spring_security_remember_me": "true",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        "Referer": "http://openlaw.cn/login.jsp",
    }
    sess.request("POST", url=sign_in_url, headers=headers, data=data)

    profile_url = "http://openlaw.cn/user/profile.jsp"
    response = sess.request("GET", url=profile_url, headers=headers)
    if "注册日期" in response.text:
        print("登录成功")

def get_progress_id():
    # 获取 progress id
    download_url = "http://openlaw.cn/progress.jsp"
    querystring = {"showResults": "true",
                   "keyword": key_word,
                   "causeId": "",
                   "caseNo": "",
                   "litigationType": "",
                   "docType": "",
                   "litigant": "",
                   "plaintiff": "",
                   "defendant": "",
                   "thirdParty": "",
                   "lawyerId": "",
                   "lawFirmId": "",
                   "legals": "",
                   "courtId": "",
                   "judgeId": "",
                   "clerk": "",
                   "judgeDateYear": "",
                   "judgeDateBegin": judgeDateBegin,
                   "judgeDateEnd": judgeDateEnd,
                   "zone": province_name,
                   "procedureType": "",
                   "lawId": "",
                   "lawSearch": "",
                   "courtLevel": "",
                   "judgeResult": "",
                   "page": start_page
                   }

    headers = {
        'Host': "openlaw.cn",
        'Referer': "http://openlaw.cn/login.jsp?$=deny",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }

    response = sess.request("GET", download_url, headers=headers, params=querystring)
    # print(response.text)
    progress_id = re.findall(r'queryProgress\("(.*?)"\);', response.text)[0]
    print("progress_id -> {}".format(progress_id))
    progress_csrf_value = re.findall("csrf=(.*?)&size=", response.text)[0]
    print("progress_csrf_value -> {}".format(progress_csrf_value))
    return progress_id, progress_csrf_value


def signal():
    signal_url = "http://openlaw.cn/progressManager.jsp?progressId={}".format(progress_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }
    sess.request("GET", signal_url, headers=headers)


def output_file():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }
    output_url = "http://openlaw.cn/service/rest/opendata.Judgement/collection/xlsx"
    querystring = {
        "_csrf": progress_csrf_value,
        "size": size,
        "action": "xlsx",
        "progressId": progress_id,
        "showResults": "true",
        "keyword": key_word,
        "causeId": "",
        "caseNo": "",
        "litigationType": "",
        "docType": "",
        "litigant": "",
        "plaintiff": "",
        "defendant": "",
        "thirdParty": "",
        "lawyerId": "",
        "lawFirmId": "",
        "legals": "",
        "courtId": "",
        "judgeId": "",
        "clerk": "",
        "judgeDateYear": "",
        "judgeDateBegin": judgeDateBegin,
        "judgeDateEnd": judgeDateEnd,
        "zone": province_name,
        "procedureType": "",
        "lawId": "",
        "lawSearch": "",
        "courtLevel": "",
        "judgeResult": "",
        "page": start_page,
    }
    response = sess.request("POST", output_url, headers=headers, params=querystring)
    print(response.text)


def output_signal():
    output_signal_url = "http://openlaw.cn/progressManager.jsp?progressId={}".format(progress_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }
    response = sess.request("GET", output_signal_url, headers=headers)
    print(response.text)
    print("正在导出...")


def down_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }
    down_data_url = "http://openlaw.cn/service/rest/tk.File/{}/download".format(progress_id)
    print("下载链接: {}".format(down_data_url))
    response = sess.request("GET", down_data_url, headers=headers)
    with open("./data.xlsx", "wb") as f:
        f.write(response.content)
    print("下载成功~")


key_word = "投资"
province_name = "河南省"
start_page = "1"
size = "30"
judgeDateBegin = "2018-01-01"
judgeDateEnd = "2018-02-01"

sess = requests.Session()
csrf_value = get_csrf_value()
verify_value = get_verify_value()
login()
progress_id, progress_csrf_value = get_progress_id()
signal()
output_file()
output_signal()
time.sleep(120)
down_data()
