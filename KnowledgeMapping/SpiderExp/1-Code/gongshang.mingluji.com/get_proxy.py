import requests


url = "http://47.106.170.4:8081/Index-generate_api_url.html?packid=1&fa=0&qty=1&port=1&format=txt&ss=3&css=&ipport=1&pro=&city="

while True:
    response = requests.get(url=url)
    if "请求太频繁" in response.text:
        print(response.text)
    else:
        print(response.text)
        break

