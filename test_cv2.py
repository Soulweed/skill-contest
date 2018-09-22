
#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import time
import numpy as np
cap = cv2.VideoCapture(0)
#mat = cv2.imread("/home/pi/peas1/skill-contest/Tranformer/138885245286.jpg")
#cv2.imshow('Window',mat)
#cv2.startWindowThread()
#cv2.namedWindow("image")
while True:
	ret, frame = cap.read()
	#cv2.imwrite("/home/pi/peas1/skill-contest/live.jpg",frame)
	#cv2.waitKey()
	#mat = cv2.imread("/home/pi/peas1/skill-contest/live.jpg")
	#cv2.startWindowThread()
	#cv2.namedWindow("image")
#	cv2.imshow("image", frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	#cv2.destroyAllWindows()
	cv2.imshow("image", frame)

cap.release()
cv2.destroyAllWindows()
