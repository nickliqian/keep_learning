import cv2
import numpy as np

img1 = cv2.imread('45.jpg')

e1 = cv2.getTickCount()
# for i in range(5, 49, 2):
#     img1 = cv2.medianBlur(img1,i)

# 模糊化-中值滤波
img1 = cv2.medianBlur(img1, 41)


e2 = cv2.getTickCount()
t = (e2-e1)/cv2.getTickFrequency()
print(t)

cv2.imshow('res', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 查看默认优化是否开启
print(cv2.useOptimized())