#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy
from matplotlib import pyplot as plt

# 读取图片
img = cv2.imread('45.jpg')
# 获取指定位置的像素值
px = img[100, 100]
print(px)
# 获取指定位置指定通道的像素值
blue = img[100, 100, 0]
print(blue)
# 修改指定位置的像素值
img[101, 101] = [255, 255, 255]
print(img[101, 101])

print(type(img))
print(img.shape)

print("===")
print(img.item(100, 100, 2))
img.itemset((100, 100, 2), 100)
print(img.item(100, 100, 2))

print("===")
print(img.shape)  # 图像的形状，返回值是一个包含行数，列数，通道数的元组

print("===")
print(img.size)  # 像素数量

print("===")
print(img.dtype)  # 图像数据类型

# ball = img[20:30, 30:30]
# img[40:40, 50:50] = ball

plt.imshow(img)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()