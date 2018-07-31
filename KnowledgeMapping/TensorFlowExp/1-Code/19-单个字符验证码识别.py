# -*- coding: utf-8 -*-
# @Topic : 
# @Title : 
# @Content : 
# @Author : LiQian
# @Create Time : 2018/07/31 19:29
# @Update Time : 2018/07/31 19:29
from PIL import Image, ImageDraw


# 二值化
def threshold_img(img, threshold):
    img = img.convert("L")
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    # convert to binary image by the table
    img = img.point(table, "1")
    return img


def depoint(img):
    """传入二值化后的图片进行降噪"""
    pixdata = img.load()
    w, h = img.size
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            count = 0
            if pixdata[x, y - 1] > 245:  # 上
                count = count + 1
            if pixdata[x, y + 1] > 245:  # 下
                count = count + 1
            if pixdata[x - 1, y] > 245:  # 左
                count = count + 1
            if pixdata[x + 1, y] > 245:  # 右
                count = count + 1
            if pixdata[x - 1, y - 1] > 245:  # 左上
                count = count + 1
            if pixdata[x - 1, y + 1] > 245:  # 左下
                count = count + 1
            if pixdata[x + 1, y - 1] > 245:  # 右上
                count = count + 1
            if pixdata[x + 1, y + 1] > 245:  # 右下
                count = count + 1
            if count > 4:
                pixdata[x, y] = 255
    return img


def main():
    root_dir = "/home/nick/Desktop/jupyterNotebook/data/cp2/0/1.png"
    img = Image.open(root_dir)
    img = img.convert("L")
    img.show()
    im = threshold_img(img, 150)
    im.show()
    im = depoint(im)
    im.show()


if __name__ == '__main__':
    main()
