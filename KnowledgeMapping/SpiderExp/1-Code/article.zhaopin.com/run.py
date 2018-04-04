import requests


url = "http://article.zhaopin.com/payquery/pay_query.do"

params = {
    "ps.type": "1",  # 求职者 or 毕业生
    "ps.cityId": "440300",  # 地区id
    "ps.callingId": "27",  # 行业
    "ps.corpPropertyId": "4",  # 公司类型
    "ps.jobCatId": "10",  # 职位类别
    "ps.jobLevelId": "4",  # 职位级别
    "pur.amount": "10000",  # 期望月薪
    "ps.apiType": "api",
}

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}

response = requests.get(url=url, params=params, headers=headers, timeout=6)

print(response.text)
