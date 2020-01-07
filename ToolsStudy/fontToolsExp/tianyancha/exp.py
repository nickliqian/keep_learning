# -*- coding: utf-8 -*-
# @Topic : 
# @Title : 
# @Content : 
# @Author : LiQian
# @Create Time : 2018/08/17 17:46
# @Update Time : 2018/08/17 17:46
import requests
from fontTools.ttLib import TTFont


url = "https://StaticFile.tianyancha.com/fonts-styles/fonts/b1/b17d9d87/tyc-num.woff"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
}
r = requests.get(url, headers=headers)
with open("./font.woff", "wb") as f:
    f.write(r.content)


url = "https://StaticFile.tianyancha.com/fonts-styles/fonts/b1/b17d9d87/tyc-num.ttf"

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
}
r = requests.get(url, headers=headers)
with open("./font.ttf", "wb") as f:
    f.write(r.content)


online_fonts = TTFont('font.woff')

online_fonts.saveXML("text.xml")

_dict = online_fonts.getBestCmap()

print("字典:", _dict)


# online_fonts = TTFont('font.tff')
#
# online_fonts.saveXML("text.xml")
#
# _dict = online_fonts.getBestCmap()
#
# print("字典:", _dict)