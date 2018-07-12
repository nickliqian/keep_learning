#!/usr/bin/python
# -*- coding: UTF-8 -*-
import cv2
import numpy as np
from matplotlib import pyplot as plt

x = np.uint8([250, 100])
y = np.uint8([10, 9])

print(x)
print(y)

print(cv2.add(x, y))  # 250+10=260>=255  加法后转置
# 结果为[[255]]
print(x + y)  # 250+10=260%255=4  加法后取模
# 结果为[4]
print("===")

img1 = cv2.imread('45.jpg')
img2 = cv2.imread('46.jpg')

print(img1.shape)
print(img2.shape)

h = img1.shape[0]
w = img1.shape[1]

img2 = cv2.resize(img2, (w, h), interpolation=cv2.INTER_CUBIC)


dst = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)

cv2.imshow('dst', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
