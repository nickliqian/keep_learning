import cv2
import numpy as np


# 原图
img = cv2.imread("./48.jpg")

# 1. HSV 分离颜色
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


# 2. 对hsv根据阀值转换
# 设定颜色的阀值
lower_blue = np.array([50, 50, 50])
upper_blue = np.array([130, 100, 100])
# 根据阀值构建掩模
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# 3. 对原图和掩模进行位运算
res = cv2.bitwise_and(img, img, mask=mask)

# 显示图像
cv2.imshow('frame', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('hsv', hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow('res', res)
cv2.waitKey(0)
cv2.destroyAllWindows()

