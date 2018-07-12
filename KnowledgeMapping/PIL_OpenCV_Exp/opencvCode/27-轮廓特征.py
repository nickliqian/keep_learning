import numpy as np
import cv2


def show_img(im, name="no name"):
    cv2.imshow(name, im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img = cv2.imread('48.jpg', 0)
ret, thresh = cv2.threshold(img, 50, 255, 0)

show_img(thresh)

image, contours, hierarchy = cv2.findContours(thresh, 1, 2)

cnt = contours[0]
M = cv2.moments(cnt)
print(M)

cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print(cx, cy)

area=cv2.contourArea(cnt)
print(area)
perimeter = cv2.arcLength(cnt,True)
print(perimeter)

epsilon=0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)

print(epsilon)
print(approx)

x,y,w,h=cv2.boundingRect(cnt)
img1=cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
show_img(img1)