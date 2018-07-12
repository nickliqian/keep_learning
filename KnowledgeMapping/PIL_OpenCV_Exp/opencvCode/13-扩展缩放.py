import cv2

img = cv2.imread('45.jpg')
# 下面的None本应该是输出图像的尺寸，但是因为后面我们设置了缩放因子，所以，这里为None
# res = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
# or
# 这里直接设置输出图像的尺寸，所以不用设置缩放因子
height, width = img.shape[:2]
res = cv2.resize(img, (int(0.5*width), int(0.5*height)), interpolation=cv2.INTER_CUBIC)

while True:
    cv2.imshow('res', res)
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()
