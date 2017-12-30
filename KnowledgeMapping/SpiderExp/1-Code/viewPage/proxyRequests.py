import requests

proxies = {
    "http": "121.31.197.207:8123",
}
url = "http://www.httpbin.org/ip"
r = requests.get(url=url, proxies=proxies)
print(r.text)