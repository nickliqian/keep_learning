import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('47.jpg', 0)
edges = cv2.Canny(img, 100, 200, L2gradient=False)

plt.subplot(121), plt.imshow(img, cmap='gray')
plt.title('original'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(edges, cmap='gray')
plt.title('edge'), plt.xticks([]), plt.yticks([])

plt.show()
