import cv2
import numpy as np
from matplotlib import pyplot as plt

# 原图
img = cv2.imread('49.jpg')
cv2.imshow('frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 平均-归一化
blur1 = cv2.blur(img, (5, 5))
cv2.imshow('frame', blur1)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 高斯模糊
blur2 = cv2.GaussianBlur(img, (5, 5), 0)
cv2.imshow('frame', blur2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 中值模糊
median = cv2.medianBlur(img,5)
cv2.imshow('frame', median)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 双边滤波
blur3 = cv2.bilateralFilter(img,9,75,75)
cv2.imshow('frame', blur3)
cv2.waitKey(0)
cv2.destroyAllWindows()