import requests
import time
import random

url = "http://www1.soopat.com/Account/ValidateImage"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
}

for i in range(100):
    while True:
        try:
            response = requests.get(url, headers=headers, proxies={"http": "117.78.31.36:1080"}, timeout=10)
            break
        except Exception as e:
            print(e)

    name = "{}_{}".format(random.randint(0, 100), time.time())

    with open("/home/nick/Desktop/jupyterNotebook/captcha_soopat.com/{}.gif".format(name), "wb") as f:
        f.write(response.content)
    print("{} > Get image {}".format(i, name))
    time.sleep(1.5)
