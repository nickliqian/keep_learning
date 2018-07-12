import cv2
import numpy as np
from matplotlib import pyplot as plt




img = cv2.imread('48.jpg', 0)
# 中值滤波
img = cv2.medianBlur(img, 5)

ret, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('1', th1)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 11为block size，2为C值
th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
cv2.imshow('2', th2)
cv2.waitKey(0)
cv2.destroyAllWindows()

th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
cv2.imshow('3', th3)
cv2.waitKey(0)
cv2.destroyAllWindows()
