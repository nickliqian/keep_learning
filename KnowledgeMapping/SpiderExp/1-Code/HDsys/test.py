import requests


url = "http://yxxt.hainu.edu.cn/web/XsLogin/Login"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64)"
                  " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referer": "http://yxxt.hainu.edu.cn/web/home"
}
data = {
    "u": "20172783310164",
    "p": "190318",
    "c": "hfjv",
    "d": "XH",
}

# 构造会话
sess = requests.session()

# 请求验证码
response = sess.get(url="http://yxxt.hainu.edu.cn/login/code?i=", headers=headers)

with open("./cp.jpg", "wb") as f:
    f.write(response.content)


cp_text = input("输入验证码：")
data["c"] = str(cp_text)
response = sess.post(url=url, headers=headers, data=data)
print(response)

print(response.text)

print("++++++++++++++++")
print("++++++++++++++++")
print("++++++++++++++++")


url2 = "http://yxxt.hainu.edu.cn/web/home/xszzIndex"
response = sess.get(url=url2, headers=headers)
print(response)
print(response.text)


# 个人信息
url_person_info = "http://yxxt.hainu.edu.cn/XS/XSXSXX/YXGRXX"
# 宿舍信息
url_person_room = "http://yxxt.hainu.edu.cn/XS/CW/Detail"
# 同伴查询
url_person_friend = "http://yxxt.hainu.edu.cn/XS/XSXSXX/TXXX"
