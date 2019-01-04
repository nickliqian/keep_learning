#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import pytesseract
from PIL import Image
from io import BytesIO


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"
}
url = "http://static8.ziroom.com/phoenix/pc/images/price/e72ac241b410eac63a652dc1349521fd.png"

response = requests.get(url=url, headers=headers)

with open("test.png", "wb") as f:
    f.write(response.content)

image = BytesIO(response.content)
im = Image.open(image)
text = pytesseract.image_to_string(im, lang="eng", config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789")
print(text)