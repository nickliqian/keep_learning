import numpy as np
import cv2
from matplotlib import pyplot as plt
# 读取文件和显示图形
img = cv2.imread('45.jpg', 0)
plt.imshow(img, cmap='gray', interpolation='bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()

# 保存图片
# cv2.imwrite('46.png',img)