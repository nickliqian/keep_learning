#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import pytesseract
from PIL import Image
from io import BytesIO
import json


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
}

url = "http://www.ziroom.com/detail/info?id=60992917&house_id=60159768"
response = requests.get(url=url, headers=headers)
text = response.json()
static_url = text["data"]["price"]
ima_url = "http:" + static_url[1]
price_num = static_url[2]

response = requests.get(url=ima_url, headers=headers)

with open("test.png", "wb") as f:
    f.write(response.content)

image = BytesIO(response.content)
im = Image.open(image)
text = pytesseract.image_to_string(im, lang="eng", config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789")
print(text)
price = ""
for i in price_num:
    price += text[i]

print(price)