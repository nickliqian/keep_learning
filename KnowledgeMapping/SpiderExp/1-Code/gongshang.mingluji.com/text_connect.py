import requests


# response = requests.get(url="http://httpbin.org/ip", proxies={"http": "113.121.246.159:21709"})
response = requests.get(url="http://httpbin.org/ip")



print(response.text)
