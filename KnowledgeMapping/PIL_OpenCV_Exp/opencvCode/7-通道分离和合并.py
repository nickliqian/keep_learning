#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy
from matplotlib import pyplot as plt

# 读取图片
img = cv2.imread('45.jpg')
origin_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

r, g, b = cv2.split(origin_img)  # 拆分
merged = cv2.merge([b, r, g])
# cv2.imshow("merged", merged)

plt.imshow(merged)
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()