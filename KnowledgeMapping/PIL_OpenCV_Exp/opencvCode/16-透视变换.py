import cv2
import numpy as np
from matplotlib import pyplot as plt


img = cv2.imread('45.jpg')
rows, cols, ch = img.shape

# 对于视角变换，我们需要一个3x3变换矩阵。
# 在变换前后直线还是直线。需要在原图上找到4个点，以及他们在输出图上对应的位置，这四个点中任意三个都不能共线，
pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])

M = cv2.getPerspectiveTransform(pts1, pts2)
dst = cv2.warpPerspective(img, M, (300, 300))

cv2.imshow('res', dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

# plt.subplot(121, plt.imshow(img), plt.title('Input'))
# plt.subplot(121, plt.imshow(img), plt.title('Output'))
# plt.show()
