import requests
import re



task = []
seen = set()

def run(url):
    print("Get -> {}".format(url))
    response = requests.get(url)
    urls = re.findall(r'<a\shref="(/.*?|http://www\.traincode*?|http://traincode*?)".*?>.*?</a>', response.text)

    for url in urls:
        if url.startswith("/"):
            url = "http://www.traincode.cn" + url

        if url not in seen:
            seen.add(url)
            run(url)

s_url = "http://www.traincode.cn/"
run(s_url)
print("=========")
print(seen)