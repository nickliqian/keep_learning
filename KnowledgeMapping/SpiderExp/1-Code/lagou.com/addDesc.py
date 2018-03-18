import json
import requests
import time
import re
import redis


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Cookie": "_ga=GA1.2.454316681.1519021371; user_trace_token=20180219142252-50b13d09-153d-11e8-b074-5254005c3644; LGUID=20180219142252-50b142ff-153d-11e8-b074-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAIAACBI61131395D7911EB97CE48A6D7E95E463; _gid=GA1.2.1019274703.1521289277; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519021372,1520398935,1520943879,1521289277; TG-TRACK-CODE=jobs_code; LGSID=20180318224733-4a769a36-2abb-11e8-b446-5254005c3644; X_HTTP_TOKEN=ab3c15fa7fe2929b07bc0ed1bc0916ae; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521386336; LGRID=20180318231855-ac70f062-2abf-11e8-8524-525400f775ce",
    "Host": "www.lagou.com",
    "Pragma": "no-cache",
    "Referer": "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?px=default&city=%E5%85%A8%E5%9B%BD",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
}

redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, db=1)
conn_redis = redis.Redis(connection_pool=redis_pool)
sess = requests.session()

i = 0
while True:

    # conn_redis.lpop("lagou:spider")
    data = conn_redis.lindex("lagou:spider", i)
    data = data.decode("utf-8")

    if data:

        try:
            item = json.loads(data)
        except Exception:
            print("有未转义的词语，跳过")
            i += 1
            continue

        # 选择id
        page_id = item["positionId"]
        # 判断是否有成功采集过
        desc = item.get("desc", "ReErrorNull")
        # 没有成功采集过
        if desc == "" or desc == "ReErrorNull":
            print("<id：{}>, desc is {}, crawl desc info".format(page_id, desc))
            # 请求链接
            url = "https://www.lagou.com/jobs/{}.html".format(page_id)
            while True:
                try:
                    response = sess.request("get", url=url, headers=headers)
                    if response.status_code == 200 or response.text != "":
                        break
                except Exception as e:
                    print(type(e))
                    print(e)
            # 解析内容
            pattern = r'<dd\sclass="job_bt">(.*?)</dd>'
            desc = re.findall(pattern, response.text, re.S)
            if desc:
                data = desc[0].replace("\n", "")
                re_data = re.sub(r"<p.*?>|</p>|<div.*?>|</div>|<h3.*?>|</h3>|\s|<br.*?>|<li.*?>|<ul.*?>|<strong.*?|\&nbsp;>", "", data)
                item["desc"] = re_data
            else:
                print("Re error")
                item["desc"] = "ReErrorNull"
            print(item)
            # conn_redis.rpush("lagou:spider", result_data)
            conn_redis.lset("lagou:spider", i, str(item))

        # 采集成功的条目
        else:
            print("skip <id：{}>".format(page_id))
    else:
        print("Redis no data")

    i += 1
    time.sleep(1)





