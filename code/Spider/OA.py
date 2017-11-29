import requests
import datetime
import time


# my_date = "2017-11-24"
def get_today_wt(my_date):
    if not my_date:
        a = my_date + ' 00:00:00'
    else:
        a = datetime.datetime.now().strftime('%Y-%m-%d') + ' 00:00:00'
    timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
    # eachday
    workTime = time.mktime(timeArray) * 1000
    workTime = str(int(workTime))
    return workTime

url = 'https://oa.shijinshi.cn/sjsinfo/main/login'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Host': 'oa.shijinshi.cn',
    'Referer': 'https://oa.shijinshi.cn/sjsinfo/main/login',
}
login_data = {
    "username": "liqian",
    "password": "1234qwer",
}

sess = requests.session()
r = sess.post(url, headers=headers, data=login_data, verify=False)



work_data = {
    'workType': '62',
    'name': '项目开发',
    'type.id': '62',
    'workTime': get_today_wt("2017-11-03"),
    'project.id': '',
    'duration': '8',
    'remarks': 'CMDB系统开发',
    'overTime': '0',
}
its_url = 'https://oa.shijinshi.cn/sjsinfo/main/oa/timeSheet/insertTimeSheet'
r = sess.post(its_url, data=work_data, verify=False)
print(r.status_code)