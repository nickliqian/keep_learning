import cv2


img = cv2.imread('45.jpg', 0)
rows, cols = img.shape
# 这里的第一个参数为旋转中心，第二个为旋转角度，第三个为旋转后的缩放因子
# 可以通过设置旋转中心，缩放因子以及窗口大小来防止旋转后超出边界的问题。
# 设置一个缩放的画布 第一个参数指定旋转的中心
M = cv2.getRotationMatrix2D((cols/2, rows/2), 10, 0.6)
# 第三个参数是输出图像的尺寸中心
# 把图片塞进去M，同时指定输出大小
dst = cv2.warpAffine(img, M, (cols, rows))

while True:
    cv2.imshow('img', dst)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
