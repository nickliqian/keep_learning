import requests
import re


url = "http://bj.58.com/ershoufang/31973214988731x.shtml?from=1-list-0&iuType=d_2&PGTID=0d300000-0000-0f38-dad6-8b7f59142649&ClickID=1"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
}
response = requests.get(url=url, headers=headers)

# print(response.text)

results = re.findall(r'____json4fe\.xiaoquSubway\s=\s\["(.*?)","(.*?)"\];', response.text)

for i in results[0]:
    print(i.encode('utf-8').decode('unicode_escape'))