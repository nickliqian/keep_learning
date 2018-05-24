import requests

url = "https://www.tianyancha.com/pagination/invest.xhtml"

querystring = {"ps":"20","pn":"2","id":"24416401","_":"1527059174821"}

headers = {
    'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
    'x-requested-with': "XMLHttpRequest",
    'Cache-Control': "no-cache",
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)