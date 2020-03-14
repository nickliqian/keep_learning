import requests


r = requests.get(url="http://127.0.0.1:6666/")

print(r.text)
print(r.status_code)