import requests


# data
# acount
post_info = {
    "username": "liqian",
    "password": "LQ@yzm2019",
    "rememberMe": "on"
}

login_url = "https://oa.shijinshi.cn/sjsinfo/main/login"
login_headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'content-length': "51",
    'content-type': "application/x-www-form-urlencoded",
    'dnt': "1",
    'host': "oa.shijinshi.cn",
    'origin': "https://oa.shijinshi.cn",
    'pragma': "no-cache",
    'referer': "https://oa.shijinshi.cn/sjsinfo/main/login",
    'sec-fetch-mode': "navigate",
    'sec-fetch-site': "same-origin",
    'sec-fetch-user': "?1",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

card_url = "https://oa.shijinshi.cn/sjsinfo/main/oa/workClockInRecord/clockInOrOut"
card_headers = {
    'accept': "*/*",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'content-length': "0",
    'dnt': "1",
    'host': "oa.shijinshi.cn",
    'origin': "https://oa.shijinshi.cn",
    'pragma': "no-cache",
    'referer': "https://oa.shijinshi.cn/sjsinfo/main?login",
    'sec-fetch-mode': "cors",
    'sec-fetch-site': "same-origin",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    'x-requested-with': "XMLHttpRequest",
    }

# obj
session = requests.session()

# login
response = session.post(url=login_url, headers=login_headers, data=post_info, verify=False, timeout=8)
if "我的通知" in response.text:
    print("登录成功")
else:
    print("登录失败")

response = session.post(url=card_url, headers=card_headers, verify=False, timeout=8)
if response.text == "in":
    print("success")
else:
    print("打卡失败")




