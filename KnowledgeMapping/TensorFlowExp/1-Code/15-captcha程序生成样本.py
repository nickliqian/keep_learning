# -*- coding: utf-8 -*-
# @Topic : 
# @Title : 
# @Content : 
# @Author : LiQian
# @Create Time : 2018/07/31 14:24
# @Update Time : 2018/07/31 14:24
from captcha.image import ImageCaptcha
import matplotlib.pyplot as plt
import numpy as np
import random
import string
from PIL import Image, ImageDraw
import os


# def gen_random_img():
#     root_dir = "/home/nick/Desktop/jupyterNotebook/data/cp1"
#     characters = string.digits + string.ascii_uppercase
#     print("characters", characters)
#     # 设置初始值
#     width = 40
#     height = 70
#     n_len = 1
#     n_class = len(characters)
#
#     # 生成img文件
#     generator = ImageCaptcha(width=width, height=height)  # 指定大小
#     random_str = ''.join([random.choice(characters) for j in range(n_len)])  # 生成随机文字
#     img = generator.generate_image(random_str)  # 生成图谱
#     # img.show()   # 展示图片
#     file_path = os.path.join(root_dir, "{}.png".format(random_str))
#     img.save(file_path)


def gen_special_img(text, file_path):
    # 设置初始值
    width = 50
    height = 50
    # 生成img文件
    generator = ImageCaptcha(width=width, height=height)  # 指定大小
    img = generator.generate_image(text)  # 生成图片
    img.save(file_path)


if __name__ == '__main__':
    root_dir = "/home/nick/Desktop/jupyterNotebook/data/cp2"
    characters = string.digits + string.ascii_uppercase
    characters = "0123456789"
    for cha in characters:
        cha_dir = os.path.join(root_dir, cha)
        if not os.path.exists(cha_dir):
            os.mkdir(cha_dir)
        for i in range(100):
            p = os.path.join(cha_dir, "{}.png".format(str(i)))
            gen_special_img(cha, p)

