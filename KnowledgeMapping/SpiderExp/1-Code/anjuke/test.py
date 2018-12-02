#!/usr/bin/python
# -*- coding: UTF-8 -*-
from PIL import Image


img = Image.open("C:\\Users\\李谦\\Desktop\\captcha_img.jpg")
img = img.resize((280, 158))
img.save("C:\\Users\\李谦\\Desktop\\captcha_img2.jpg")