#!/usr/bin/python
# -*- coding: UTF-8 -*-

#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
import time
from lxml import etree
import random
import string


class RunMail(object):
    def __init__(self):
        # mail_list = ["bccto.me", "11163.com", "chaichuang.com", "dawin.com", "a7996.com", "4057.com", "3202.com",
        #              "juyouxi.com", "zymuying.com", "jnpayy.com", "cuirushi.org", "4059.com", "ytpayy.com",
        #              "zhaoyuanedu.cn", "dhy.cc", "dhy.cc", "dongqing365.com", "dongqing365.com", "cr219.com",
        #              "cr219.com"]
        mail_list = ["dawin.com"]
        self.mail_prefix = self.random_string()
        self.mail_postfix = random.choice(mail_list)
        self.mail = "{}@{}".format(self.mail_prefix, self.mail_postfix)
        print("Get Mail   <{}>".format(self.mail))
        self.sess = requests.Session()

    def run(self):
        self.keep_session()
        apply_status = self.apply_mail()
        if not apply_status:
            return
        # init mail string
        url_mail_postfix = self.mail_postfix.replace(".", "-_-")
        mail_string = "{}(a){}".format(self.mail_prefix, url_mail_postfix)
        print("Generate mail string <{}>".format(mail_string))
        # check mail and receive mail
        msg = self.check_mail()
        # get mail page url
        href = "http://mail.bccto.me/win/{}/{}".format(mail_string, msg)
        print(href)
        print("Mail page url <{}>".format(href))
        # 请求邮件，抽取激活地址
        active_href = self.req_mail_href(href)
        # 请求激活地址
        self.req_active_href(active_href)

    @staticmethod
    def random_string():
        num = random.randint(7, 13)
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, num))
        # return ran_str
        return "0bmomfiwkq"

    # Get cookies
    def keep_session(self):
        url = "http://www.bccto.me/"
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Host': "www.bccto.me",
            'Pragma': "no-cache",
            'Referer': "https://www.baidu.com/link?url=Ec_jowVsHws7ayJ5E9PhdIf2LvFZ36lGea6uidXWwwe&wd=&eqid=8a965ba20003c948000000065b505f3c",
            'Upgrade-Insecure-Requests': "1",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
        }
        self.sess.request("GET", url, headers=headers, timeout=60)
        print("Keep Session")

    # Apply mail
    def apply_mail(self):
        url = "http://www.bccto.me/applymail"
        payload = {
            "mail": self.mail,
        }
        print(payload)
        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Content-Length': "31",
            'Content-Type': "application/x-www-form-urlencoded",
            'Host': "www.bccto.me",
            'Origin': "http://www.bccto.me",
            'Pragma': "no-cache",
            'Referer': "http://www.bccto.me/",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
        }
        response = self.sess.request("POST", url, data=payload, headers=headers, timeout=60)
        print(response.text)
        response_json = json.loads(response.text)
        req_mail_status = response_json["success"]
        if req_mail_status:
            print("Apply mail success")
            return True
        else:
            print("requests mail failed")
            return False

    # Monitor mail
    def check_mail(self):
        url = "http://www.bccto.me/getmail"
        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            'Cache-Control': "no-cache",
            'Connection': "keep-alive",
            'Content-Length': "63",
            'Content-Type': "application/x-www-form-urlencoded",
            'Host': "www.bccto.me",
            'Origin': "http://www.bccto.me",
            'Pragma': "no-cache",
            'Referer': "http://www.bccto.me/",
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest",
        }
        while True:
            var_a = str(time.time()).replace(".", "")[:-7]
            var_b = str(time.time()).replace(".", "")[:-4]
            data = {
                "mail": str(self.mail),
                "time": var_a,
                "_": var_b,
            }
            response = self.sess.request("POST", url=url, headers=headers, data=data, timeout=15)
            print(response.text)
            try:
                r_data = json.loads(response.text)
            except json.decoder.JSONDecodeError:
                if "NO NEW MAIL" in response.text:
                    time.sleep(2)
                    continue
                else:
                    raise TypeError("未知错误")
            result = r_data["mail"]
            if result:
                print("Get mail -> {}".format(result))
                return result[0][4]
            else:
                print("No mail")
            time.sleep(2)

    def req_mail_href(self, mail_href):
        headers = {
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9",
            'cache-control': "no-cache",
            'host': "mail.bccto.me",
            'pragma': "no-cache",
            'proxy-connection': "keep-alive",
            'upgrade-insecure-requests': "1",
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        }
        response = requests.get(url=mail_href, headers=headers)
        # print(response.text)
        html = etree.HTML(response.text)
        active_href = html.xpath("//a/@href")[0]
        print(active_href)
        return active_href

    def req_active_href(self, active_href):
        headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        }
        response = requests.get(url=active_href, headers=headers)
        print(response.text)
        html = etree.HTML(response.text)
        active_href = html.xpath("//a/@href")[0]
        print(active_href)
        return active_href


if __name__ == '__main__':
    r = RunMail()
    r.run()
