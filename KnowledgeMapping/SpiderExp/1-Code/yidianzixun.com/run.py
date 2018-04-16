import requests
import json
import execjs


url = "http://www.yidianzixun.com/home/q/news_list_for_channel"
params = {
    "channel_id": "11743365582",
    "cstart": "10",
    "cend": "20",
    "infinite": "true",
    "refresh": "1",
    "__from__": "pc",
    "multi": "5",
    "appid": "web_yidian",
    "_": "1523865295265",
}

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cache-Control": "no-cache",
    "Host": "www.yidianzixun.com",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://www.yidianzixun.com/channel/c11",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

cookies = {
    "JSESSIONID": "0d57b6fcd023c01f67716525f5b64a0d1d05935d5c0ae1a130272e6b295109f7",
    "wuid": "289895602574831",
    "wuid_createAt": "2018-04-16 15:51:19",
    "weather_auth": "2",
    "Hm_lvt_15fafbae2b9b11d280c79eff3b840e45": "1523865079",
    "UM_distinctid": "162cd6fd0c7ac9-02d7cb015c9144-3b7c015b-1fa400-162cd6fd0c8f9b",
    "CNZZDATA1255169715": "268439245-1523861655-%7C1523861655",
    "Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45": "1523865295",
    "captcha": "s%3A059f3736ab053acaf973b50ce3fd509d.IDh1%2FtV8lF0oxw2LfyCZldtNxVcwsddKix3vlz3E3jw",
    "cn_1255169715_dplus": "%7B%22distinct_id%22%3A%20%22162cd6fd0c7ac9-02d7cb015c9144-3b7c015b-1fa400-162cd6fd0c8f9b%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201523865294%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201523865294%7D%7D",
    "sptoken": "U%3B%3B%3D%3E99%3C%3F%3F28U%3B%3AU8%3AU48261efeced332cc9f20413132c69381e96e4aafcc39a24366a39c806f2d8efa",
}

ctx = execjs.compile("""
     function test(n, e, i) {
            t = "U;;=>99<??28U;:U8:U48261efeced332cc9f20413132c69381e96e4aafcc39a24366a39c806f2d8efa"
            e = e || 0,
            i = i || 10;
            for (var o = "_" + n + "_" + e + "_" + i + "_", a = "", c = 0; c < o.length; c++) {
                var r = 10 ^ o.charCodeAt(c);
                a += String.fromCharCode(r)
            }
            t = /^U.+?U.{1,3}U.{1,3}U/.test(t) ? t.replace(/^U.+?U.{1,3}U.{1,3}U/, a) : a + t,
            co = "sptoken=" + encodeURIComponent(t) + ";domain=.yidianzixun.com;path=/;max-age=2592000"
            co1 = encodeURIComponent(t)
            return co1;
        }
     """)

# 第一页到第五页
for i in range(1, 6):
    channel_id = "11743365582"
    start_page = (i-1)*10
    end_page = i*10

    cookies["sptoken"] = ctx.call("test", channel_id, start_page, end_page)
    params["cstart"] = str(start_page)
    params["cend"] = str(end_page)

    response = requests.get(url=url, headers=headers, params=params, cookies=cookies)
    print(response.status_code)
    result = json.loads(response.text)
    s = result["result"]
    for i in s:
        print(i)

