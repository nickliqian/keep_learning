import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('48.jpg', 0)

_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('THRESH_BINARY', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('THRESH_BINARY_INV', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_TRUNC)
cv2.imshow('THRESH_TRUNC', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO)
cv2.imshow('THRESH_TOZERO', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_TOZERO_INV)
cv2.imshow('THRESH_TOZERO_INV', thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()


# titles = ['original image', 'Binary', 'binary-inv', 'trunc', 'tozero', 'tozero-inv']
# images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]
#
# for i in range(6):
#     plt.subplot(2, 3, i + 1), plt.imshow(images[i], 'gray')
#     plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])
#
# plt.show()
