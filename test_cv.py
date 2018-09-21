
#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import time
cap = cv2.VideoCapture(0)
mat = cv2.imread("/home/pi/peas1/skill-contest/Tranformer/138885245286.jpg")
cv2.imshow('Window',mat)
while True:
	ret, frame = cap.read()
#img = cv2.imread('C:\Users\Ive\Downloads\7.jpg',0)
	cv2.imshow("image", frame)
	cv2.waitKey(1)
	#time.sleep(1)
#cv2.destroyAllWindows()
