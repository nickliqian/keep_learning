import requests


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Cookie": "JSESSIONID=2C586459971EFB4FC647BEEDB36CA445; tk=uOuEcf8guVU_5X7ijL9DDk7_CYi89RRtpwzaMjwEpGgy9W42hu4140; route=6f50b51faa11b987e576cdb301e545c4; BIGipServerotn=1389953290.64545.0000; _jc_save_fromStation=%u6DF1%u5733%2CSZQ; _jc_save_toStation=%u5CB3%u9633%u4E1C%2CYIQ; _jc_save_fromDate=2018-01-26; _jc_save_toDate=2017-12-29; _jc_save_wfdc_flag=dc; RAIL_EXPIRATION=1515742320690; RAIL_DEVICEID=OZq6m1RWPQgjeMw0p7ArZ8WM1pZVo-Z-sffmcErexTrBSxZpyAbmZUCbPJYYTQXD-_yFNuYonpa8bzQhdLR8lY1NLBROMof3pzA8LWZwR8XgWisnuPn75h0emthAea8mEelA9e3-Mkl9gb6z2ckmJYSdl6MrJXNg; BIGipServerpassport=870842634.50215.0000",
}

sess = requests.session()
profile_url = "https://kyfw.12306.cn/otn/index/initMy12306"
r = sess.get(url=profile_url, headers=headers)

print(r.text)