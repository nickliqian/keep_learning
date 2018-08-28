# -*- coding: utf-8 -*-
# @Topic : 
# @Title : 
# @Content : 
# @Author : LiQian
# @Create Time : 2018/07/31 14:24
# @Update Time : 2018/07/31 14:24
from captcha.image import ImageCaptcha
import string
import os


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

