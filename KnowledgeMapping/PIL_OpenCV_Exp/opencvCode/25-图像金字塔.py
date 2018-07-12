import numpy as np
import cv2


def show_img(im, name="no name"):
    cv2.imshow(name, im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img = cv2.imread('48.jpg')
show_img(img)

lower_reso = cv2.pyrDown(img)
show_img(lower_reso)

higher_reso2 = cv2.pyrUp(img)
show_img(higher_reso2)