import json
import requests
import time
from lxml import etree
import re


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

source_path = "D://A//C//lagouData.csv"

sess = requests.session()

with open("D://A//C//lagouData.csv", "w", encoding="utf-8") as more_f:

    with open(source_path, "r") as f:
        while True:
            data = f.readline().strip()
            if not data:
                print("exit")
                break
            item = json.loads(data)
            page_id = item["positionId"]
            print(page_id)

            print(item.keys())

            if "desc" not in item:
                print("Create desc")
                item["desc"] = ""

            if (item["desc"] == "ReErrorNull") or (item["desc"] == ""):
                print("desc is {}".format(item["desc"]))

                url = "https://www.lagou.com/jobs/{}.html".format(page_id)

                while True:
                    try:
                        response = sess.request("get", url=url, headers=headers)
                        if response.status_code == 200 or response.text != "":
                            break
                    except Exception as e:
                        print(type(e))
                        print(e)

                pattern = r'<dd\sclass="job_bt">(.*?)</dd>'
                desc = re.findall(pattern, response.text, re.S)
                if desc:
                    data = desc[0].replace("\n", "")
                    re_data = re.sub(r"<p.*?>|</p>|<div.*?>|</div>|<h3.*?>|</h3>|\s|<br.*?>", "", data)
                    item["desc"] = re_data
                else:
                    print("Re error")
                    item["desc"] = "ReErrorNull"
                result_data = json.dumps(item, ensure_ascii=False)
                print(result_data)
                more_f.write(result_data + "\n")
                time.sleep(2)

