import cv2
import numpy as np


def show_img(im, name="no name"):
    cv2.imshow(name, im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 原图
img = cv2.imread('45.jpg', 0)
show_img(img, "origin")

# 腐蚀
kernel = np.ones((5, 5), np.uint8)
erosion = cv2.erode(img, kernel, iterations=1)
show_img(erosion, "erode")

# 膨胀
dilation = cv2.dilate(img, kernel, iterations=1)
show_img(dilation, "dilation")

# 开运算
opening = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel)
show_img(opening, "opening")

# 闭运算
closing = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
show_img(closing, "closing")

# 形态学梯度
gradient = cv2.morphologyEx(img,cv2.MORPH_GRADIENT,kernel)
show_img(gradient, "gradient")

# 礼帽
tophat = cv2.morphologyEx(img,cv2.MORPH_TOPHAT,kernel)
show_img(tophat, "tophat")

# 黑帽 good
blackhat = cv2.morphologyEx(img,cv2.MORPH_BLACKHAT,kernel)
show_img(blackhat, "blackhat")