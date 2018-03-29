import requests


url = "http://qy.58.com/ajax/getBusinessInfo"
data = {
    "userName": "南京懋贸有限公司"
}
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}
r = requests.post(url=url, data=data, headers=headers)
print(r.text)