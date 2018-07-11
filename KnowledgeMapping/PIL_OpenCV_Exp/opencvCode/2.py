#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 画图形
import numpy as np
import cv2

#Create a black image
img = np.zeros((512,512,3),np.uint8)

#draw a diagonal blue line with thickness of 5 px
cv2.line(img,(0,0),(260,260),(255,0,0),5)

#为了演示，建窗口显示出来
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',1000,1000)#定义frame的大小
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

import numpy as np
import cv2

#Create a black image
img = np.zeros((512,512,3),np.uint8)

cv2.rectangle(img,(350,0),(500,128),(0,255,0),3)

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',1000,1000)#定义frame的大小
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

import numpy as np
import cv2

#Create a black image
img = np.zeros((512,512,3),np.uint8)

cv2.rectangle(img,(350,0),(500,128),(0,255,0),3)#矩形
cv2.circle(img,(425,63),63,(0,0,255),-1)#圆，-1为向内填充

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',1000,1000)#定义frame的大小
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

import numpy as np
import cv2

#Create a black image
img = np.zeros((512,512,3),np.uint8)

cv2.ellipse(img,(256,256),(100,50),0,0,360,255,-1)

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',1000,1000)#定义frame的大小
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

import numpy as np
import cv2

#Create a black image
img = np.zeros((512,512,3),np.uint8)

pts=np.array([[10,5],[20,30],[70,20],[50,10]],np.int32)
pts = pts.reshape((-1,1,2))
#这里reshape的第一个参数为-1，表明这一维度的长度是根据后面的维度计算出来的
cv2.polylines(img,[pts],True,(0,255,255))
#注意第三个参数若是False，我们得到的是不闭合的线

#为了演示，建窗口显示出来
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',1000,1000)#定义frame的大小
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

import numpy as np
import cv2

#Create a black image
img = np.zeros((512,512,3),np.uint8)

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)

#为了演示，建窗口显示出来
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image',1000,1000)#定义frame的大小
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

