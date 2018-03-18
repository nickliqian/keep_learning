import requests
import json


headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Length": "37",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_ga=GA1.2.454316681.1519021371; user_trace_token=20180219142252-50b13d09-153d-11e8-b074-5254005c3644; LGUID=20180219142252-50b142ff-153d-11e8-b074-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; JSESSIONID=ABAAABAAAIAACBI61131395D7911EB97CE48A6D7E95E463; _gid=GA1.2.1019274703.1521289277; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519021372,1520398935,1520943879,1521289277; hideSliderBanner20180305WithTopBannerC=1; _gat=1; LGSID=20180317220115-a895e8b1-29eb-11e8-b331-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E7%2588%25AC%25E8%2599%25AB%3Fpx%3Ddefault%26city%3D%25E5%2585%25A8%25E5%259B%25BD; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2F3864241.html; LGRID=20180317220150-bd63d08a-29eb-11e8-bdcc-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521295311; TG-TRACK-CODE=search_code; SEARCH_ID=27c837a1f4064093a7ff80f455c46417",
    "Host": "www.lagou.com",
    "Origin": "https://www.lagou.com",
    "Pragma": "no-cache",
    "Referer": "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?px=default&city=%E5%85%A8%E5%9B%BD",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    "X-Anit-Forge-Code": "0",
    "X-Anit-Forge-Token": "None",
    "X-Requested-With": "XMLHttpRequest",
}

url = "https://www.lagou.com/jobs/positionAjax.json"
params = {
    "px": "default",
    "needAddtionalResult": "false",
    "isSchoolJob": "0",
}
data = {
    "first": "false",
    "pn": "1",
    "kd": "爬虫",
}

sess = requests.session()

with open("D://A//C//lagouData.csv", "w") as f:
    for i in range(1, 28):

        data["pn"] = str(i)

        response = sess.request("post", url=url, headers=headers, params=params, data=data)

        data = json.loads(response.text)
        if isinstance(data, dict):
            results = data["content"]["positionResult"]["result"]

            for result in results:
                result_data = json.dumps(result, ensure_ascii=False)
                print(result_data)
                f.write(result_data + "\n")
        else:
            print("no data")
