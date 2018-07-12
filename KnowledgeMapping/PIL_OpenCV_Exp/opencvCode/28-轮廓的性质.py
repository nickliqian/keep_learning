import cv2

# 开图
img = cv2.imread('48.jpg', 0)
# 二值化
ret, thresh = cv2.threshold(img, 50, 255, 0)
# 找到轮廓
image, contours, hierarchy = cv2.findContours(thresh, 1, 2)
cnt = contours[0]
print(cnt)

x, y, w, h = cv2.boundingRect(cnt)
aspect_ratio = float(w) / h
print(aspect_ratio)

"""

1.1长宽比
边界矩形的宽高比

x,y,w,h=cv2.boundingRect(cnt)
aspect_ratio = float(w)/h
2.Extent
轮廓面积与边界矩形面积的比

area=cv2.contourArea(cnt)
x,y,w,h=cv2.boundingRect(cnt)
rect_area=w*h
extent=float(area)/rect_area
3.Solidity
轮廓面积与凸包面积的比

area=cv2.contourArea(cnt)
hull=cv2.convexHull(cnt)
hull_area=cv2.contourArea(hull)
solidity=float(area)/hull_area
4.与轮廓面积相等的圆形的直径

area=cv2.contourArea(cnt)
equi_diameter=np.sqrt(4*area/np.pi)
5.方向
对象的方向，下面的方法还会返回长轴和短轴的长度

(x,y),(MA,ma),angle=cv2.fitEllipse(cnt)
6.掩模和像素点
有时我们需要构成对象的所有像素点

mask=np.zeros(imgray.shate,np.uint8)
#这里一定要使用参数-1，绘制填充的轮廓
cv2.drawContours(mask,[cnt],0,255,-1)
pixelpoints=np.transpose(np.nonzero(mask))
7.最大值和最小值及它们的位置
可以使用掩模图像得到这些参数

min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(imgray,mask=mask)
8.平均颜色及平均灰度
同样使用相同的掩模来求得

mean_val=cv2.mean(im,mask=mask)
9.极点
一个对象最上，最下，最左，和最右的点

leftmost=tuple(cnt[cnt[:,:,0].argmin()[0])
rightmost=tuple(cnt[cnt[:,:,0].argmax()[0])
topmost=tuple(cnt[cnt[:,:,1].argmin()[0])
bottommost=tuple(cnt[cnt[:,:,1].argmax()[0])
"""
