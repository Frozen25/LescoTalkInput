#importing modules

import cv2
import numpy as np

#capturing video through webcam
cap = cv2.VideoCapture(0)

while (1):
	_, img2 = cap.read()

	#converting frame (img2 i.e BGR) to HSV (hue-saturation-value)

	hsv= cv2.cvtColor(img2,cv2.COLOR_BGR2HSV)

	#defining the range of red color
	red_lower=np.array([136,87,11],np.uint8)
	red_upper=np.array([180,255,255],np.uint8)

	#defining the range of blue color
	blue_lower=np.array([99,115,150],np.uint8)
	blue_upper=np.array([110,255,255],np.uint8)

	#defining the range of yellow color
	yellow_lower=np.array([20,60,200],np.uint8)
	yellow_upper=np.array([60,255,255],np.uint8)

	#finding the range of red,blue and yellow color in the image
	red=cv2.inRange(hsv,red_lower,red_upper)
	blue=cv2.inRange(hsv,blue_lower,blue_upper)
	yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)
	
	#Morphological transformation, Dillation
	kernal = np.ones((5,5),"uint8")

	red=cv2.dilate(red,kernal)
	Rres=cv2.bitwise_and(img2, img2, mask=red)

	blue=cv2.dilate(blue,kernal)
	Bres=cv2.bitwise_and(img2, img2, mask=blue)

	yellow=cv2.dilate(yellow,kernal)
	Yres=cv2.bitwise_and(img2, img2, mask=yellow)

	#Tracking the Red Color
	(_,contours, hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic,contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if (area > 300):
			x,y,w,h = cv2.boundingRect(contour)
			img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
			cv2.putText(img2,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255))

	#Tracking the Blue Color
	(_,contours, hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic,contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if (area > 300):
			x,y,w,h = cv2.boundingRect(contour)
			img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
			cv2.putText(img2,"BLUE color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))

	#Tracking the YELLOW Color
	(_,contours, hierarchy)=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for pic,contour in enumerate(contours):
		area = cv2.contourArea(contour)
		if (area > 300):
			x,y,w,h = cv2.boundingRect(contour)
			img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
			cv2.putText(img2,"YELLLOW color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))


	#cv2.img2show("Redcolour",red)
	cv2.imshow("Color Tracking",img2)
	#cv2.img2show("red",res)
	if cv2.waitKey(10) & 0xFF == ord('q'):
		cap.release()
		cv2.destroyALLWindows()
		break




