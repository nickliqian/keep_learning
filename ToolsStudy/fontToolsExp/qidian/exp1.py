# -*- coding: utf-8 -*-
# @Topic : 
# @Title : 
# @Content : 
# @Author : LiQian
# @Create Time : 2018/08/17 16:32
# @Update Time : 2018/08/17 16:32
from html import unescape

import requests
import os
import requests
from fontTools.ttLib import TTFont
from parsel import Selector

a = '&#100265;&#100269;&#100265;&#100264;&#100263;&#100270;'

from fontTools.ttLib import TTFont

font_type = "hLHpMjjJ"

font_url = "https://qidian.gtimg.com/qd_anti_spider/%s.woff" % font_type

woff = requests.get(font_url).content

with open('fonts.woff', 'wb') as f:
    f.write(woff)

online_fonts = TTFont('fonts.woff')

online_fonts.saveXML("text.xml")

_dict = online_fonts.getBestCmap()

print("字典:", _dict)

_dic = {
    "six": "6",
    "three": "3",
    "period": ".",
    "eight": "8",
    "zero": "0",
    "five": "5",
    "nine": "9",
    "four": "4",
    "seven": '7',
    "one": "1",
    "two": "2"
}

d = a.split(';')
cc = []
for i in d:
    if i:
        add = int(i.replace('&#', ''))
        cc.append(_dic[_dict[add]])
print("结果：", ''.join(cc))