# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 15:59:52 2018

@author: Crisptofer
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
x1,y1 = 0,0
while(1):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # define range of white color in HSV
    # change it according to your need !
    sensitivity = 15
    lower_white = np.array([0, 0, 230])
    upper_white = np.array([180, 25, 255])
    
    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= mask)
    umbral = cv2.threshold(mask, 25, 255, cv2.THRESH_BINARY)[1]
    umbral = cv2.dilate(umbral, None, iterations=2)
    
    contornosimg = umbral.copy()
    # Buscamos contorno en la imagen
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    x,y,w,h = 0,0,0,0
    
    
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if (cv2.contourArea(c) < 4000):
            continue
        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        elif(cv2.contourArea(c) > 30000):
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(c)
            # Dibujamos el rectángulo del bounds
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
	# Mostramos las imágenes de la cámara, el umbral y la resta
    if(x>(x1+50) or x<(x1-50)):
        if(x1<x):
            cv2.putText(frame,"Izquierda", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        else: 
            cv2.putText(frame,"Derecha", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        x1 = x
        
    if(y>(y1+50) or y<(y1-50)):
        if(y1<y):
            cv2.putText(frame,"Abajo", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        else:
            cv2.putText(frame,"Arriba", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
        y1 = y

    cv2.imshow('frame',frame)
    #cv2.imshow('res',umbral)
    
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()