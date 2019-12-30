import requests


url = "http://guba.eastmoney.com/news,000725,894787888.html"

headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cache-control': "no-cache",
    'connection': "keep-alive",
    'cookie': "st_si=85648086468091; qgqp_b_id=a4d4fa066eae9f6b7cfd93860f9a6896; emshistory=%5B%22%E6%BC%AB%E6%AD%A5%E8%80%85%22%5D; st_asi=delete; _adsame_fullscreen_18009=1; st_pvi=38843502416579; st_sp=2019-12-27%2023%3A29%3A41; st_inirUrl=http%3A%2F%2Fguba.eastmoney.com%2F; st_sn=89; st_psi=20191229110446106-117001300541-4211861707",
    'dnt': "1",
    'host': "guba.eastmoney.com",
    'pragma': "no-cache",
    'referer': "http://guba.eastmoney.com/list,000725_1.html",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
}

response = requests.request("GET", url, headers=headers, timeout=10, proxies=None, allow_redirects=False)

print(response.text)
print(response.status_code)
print(response.history)