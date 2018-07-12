import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('48.jpg', 0)

ret1, th1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('1', th1)
cv2.waitKey(0)
cv2.destroyAllWindows()

# good
ret2, th2 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imshow('1', th2)
cv2.waitKey(0)
cv2.destroyAllWindows()
# (5,5)为高斯核的大小，0为标准差
blur = cv2.GaussianBlur(img, (5, 5), 0)
cv2.imshow('1', blur)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 阀值一定要设为0
ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imshow('1', th3)
cv2.waitKey(0)
cv2.destroyAllWindows()


images = [img, 0, th1,
          img, 0, th2,
          img, 0, th3]
titles = ['original noisy image', 'histogram', 'global thresholding(v=127)',
          'original noisy image', 'histogram', "otsu's thresholding",
          'gaussian giltered image', 'histogram', "otus's thresholding"]
