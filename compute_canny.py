import cv2
import numpy as np

img = cv2.imread('/home/pi/openag_brain_box/img.bmp')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.GaussianBlur(img, (5, 5), 0)

canny = cv2.Canny(img, 30, 150)
cv2.imwrite('/home/pi/openag_brain_box/canny.bmp', canny)
