import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('45.jpg')
rows, cols, ch = img.shape

# 在原图中找三个点  在仿射变换中，原图中所有平行线在结果图像中同样平行
pts1 = np.float32([[50, 50], [200, 50], [50, 200]])
pts2 = np.float32([[10, 100], [200, 50], [100, 250]])
# 行，列，通道数
M = cv2.getAffineTransform(pts1, pts2)
dst = cv2.warpAffine(img, M, (cols, rows))

cv2.imshow('res', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

# plt.subplot(121, plt.imshow(img), plt.title('Input'))
# plt.subplot(121, plt.imshow(img), plt.title('output'))
# plt.show()
