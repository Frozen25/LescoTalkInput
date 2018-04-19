# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 18:43:08 2018
@author: Crisptofer
"""


import cv2
import numpy as np
import math
from csv_managment import comparate_with_database
import socket

adress = '0.0.0.0'
port = 8081

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((adress, port))
sock.listen(1)

connections = []
withAndroid = False

finger_position_list = [[], []]

def string(vec):
    result = ""
    for i in vec:
        result += str(i) + "!"

    return result

def send(message):
    for connection in connections:
        connection.send(bytes(message + "\n", 'utf-8'))

if (withAndroid):
    print("Waiting for connections")
    while True:
        client, a = sock.accept()
        connections.append(client)
        break

    print("Connected")
    print(connections)

cap = cv2.VideoCapture(0)
_, img3 = cap.read()
x1,y1 = 0,0
while(cap.isOpened()):
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
  
    # define range of white color in HSV
    # change it according to your need !
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 25, 255])
    #lower_white = np.array([0, 0, 230])
    #upper_white = np.array([180, 25, 255])
    
    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # Bitwise-AND mask and original image
    #res = cv2.bitwise_and(frame,frame, mask= mask)
    umbral = cv2.threshold(mask, 25, 255, cv2.THRESH_BINARY)[1]
    umbral = cv2.dilate(umbral, None, iterations=2)
    
    contornosimg = umbral.copy()
    # Buscamos contorno en la imagen
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    xa,ya,wa,ha = 0,0,0,0
    
    
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if (cv2.contourArea(c) < 4000):
            continue
        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        elif(cv2.contourArea(c) > 40000):
            continue
        else:
            
            (xa, ya, wa, ha) = cv2.boundingRect(c)
            # Dibujamos el rectángulo del bounds
            if(xa>40 and ya>40 and wa+80<len(frame)):
                xa-=40
                ya-=40
                wa+=80
                cv2.rectangle(frame, (xa, ya), (xa + wa, ya + ha), (0, 255, 0), 2)
                break
            else:
                cv2.rectangle(frame, (xa, ya), (xa + wa, ya + ha), (0, 255, 0), 2)
                break
 
	# Mostramos las imágenes de la cámara, el umbral y la resta
    
    """
    Aqui evaluo los movimientos, puedes sacar la información del dezsplazamiento de aquí 
    """
    horizontal = 0
    vertical = 0
    #######################################################################################
    if(xa>(x1+30) or xa<(x1-30)):
        if(x1<xa):
            cv2.putText(frame,"Izquierda", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            horizontal = -1
        else: 
            cv2.putText(frame,"Derecha", (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            horizontal = 1
        x1 = xa
        
    if(ya>(y1+30) or ya<(y1-30)):
        if(y1<ya):
            cv2.putText(frame,"Abajo", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            vertical = -1
        else:
            cv2.putText(frame,"Arriba", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
            vertical = 1
        y1 = ya
    

    #########################################################################################
    

#####################################################################    
    
    #converting frame (frame i.e BGR) to HSV (hue-saturation-value)
    direccion = 0
    #derecha
    if(horizontal == 1 and vertical == 0):
        direccion = 1 
    #izquierda
    if(horizontal == -1 and vertical == 0):
         direccion = 5 
    #arriba
    if(horizontal == 0 and vertical == 1):
        direccion = 7 
    #abajo
    if(horizontal == 0 and vertical == -1):
         direccion = 3 
    #derecha y arriba
    if(horizontal == 1 and vertical == 1):
        direccion = 8 
    #derecha y abajo
    if(horizontal == 1 and vertical == -1):
        direccion = 2 
    #izquierda y arriba
    if(horizontal == -1 and vertical == 1):
        direccion = 6 
    #izquierda y abajo
    if(horizontal == -1 and vertical == -1):
        direccion = 4 
    
    
    print(direccion, "Esta es la dirección")
    if(xa<=0 and ya<=0):
        k = cv2.waitKey(10)
        if k == 27:
            break
        else:
            cv2.imshow("Color Tracking",frame)
            continue
    
    crop_img = frame[ya:ya+ha, xa:xa+wa]
        
    hsv= cv2.cvtColor(crop_img,cv2.COLOR_BGR2HSV)
    #defining the range of red color
    red_lower=np.array([170,100,10],np.uint8)
    red_upper=np.array([180,255,255],np.uint8)

    #defining the range of blue color
    blue_lower=np.array([99,100,100],np.uint8)
    blue_upper=np.array([110,255,255],np.uint8)

    #defining the range of yellow color
    yellow_lower=np.array([20,100,100],np.uint8)
    yellow_upper=np.array([30,255,255],np.uint8)

	#defining the range of purple color
    purple_lower=np.array([124,18,91],np.uint8)
    purple_upper=np.array([152,45,140],np.uint8)

    #defining the range of green color
    green_lower=np.array([78,100,100],np.uint8)
    green_upper=np.array([96,200,200],np.uint8)

    #defining the range of black color
    black_lower=np.array([0,0,0],np.uint8)
    black_upper=np.array([120,60,61],np.uint8)

    #defining the range of oragen color
    orange_lower=np.array([8,90,96],np.uint8)
    orange_upper=np.array([18,150,225],np.uint8)

    #finding the range of red,blue and yellow color in the image
    red = cv2.inRange(hsv,red_lower,red_upper)
    blue=cv2.inRange(hsv,blue_lower,blue_upper)
    yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)
    purple=cv2.inRange(hsv,purple_lower,purple_upper)
    green=cv2.inRange(hsv,green_lower,green_upper)
    black=cv2.inRange(hsv,black_lower,black_upper)
    orange=cv2.inRange(hsv,orange_lower,orange_upper)

    #Morphological transformation, Dillation
    red = cv2.threshold(red, 25, 255, cv2.THRESH_BINARY)[1]
    red = cv2.dilate(red, None, iterations=2)

    blue = cv2.threshold(blue, 25, 255, cv2.THRESH_BINARY)[1]
    blue = cv2.dilate(blue, None, iterations=2)
    
    yellow = cv2.threshold(yellow, 25, 255, cv2.THRESH_BINARY)[1]
    yellow = cv2.dilate(yellow, None, iterations=2)
    
    purple = cv2.threshold(purple, 25, 255, cv2.THRESH_BINARY)[1]
    purple = cv2.dilate(purple, None, iterations=2)
    
    green = cv2.threshold(green, 25, 255, cv2.THRESH_BINARY)[1]
    green = cv2.dilate(green, None, iterations=2)
    
    black = cv2.threshold(black, 25, 255, cv2.THRESH_BINARY)[1]
    black = cv2.dilate(black, None, iterations=2)

    orange = cv2.threshold(orange, 25, 255, cv2.THRESH_BINARY)[1]
    orange = cv2.dilate(orange, None, iterations=2)


    red_objects, blue_objects,yellow_objects,green_objects, orange_objects, purple_objects, black_objects = [],[],[],[],[],[],[]
    
    #Tracking the Red Color
 
    contornosimg = red.copy()
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if (cv2.contourArea(c) < 200):
            continue
        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        elif(cv2.contourArea(c) > 5000):
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(c)
            # Dibujamos el rectángulo del bounds
            cv2.rectangle(frame, (xa+x, ya+y), (xa+x + w, ya+y + h), (0, 0, 255), 2)
            red_objects.append([xa+x+w/2 , ya+y+h/2])
            cv2.putText(frame,"RED color",(xa+x,ya+y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255))
        
    contornosimg = blue.copy()
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if (cv2.contourArea(c) < 200):
            continue
        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        elif(cv2.contourArea(c) > 5000):
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(c)
            # Dibujamos el rectángulo del bounds
            cv2.rectangle(frame, (xa+x, ya+y), (xa+x +w, ya+y+h), (255, 0, 0), 2)
            blue_objects.append([(xa+x + w)/2 , (ya+y+h)/2])
            cv2.putText(frame,"BLUE color",(xa+x,ya+y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))

            

    #Tracking the YELLOW Color
    
    contornosimg = yellow.copy()
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if (cv2.contourArea(c) < 200):
            continue
        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        elif(cv2.contourArea(c) > 5000):
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(c)
            # Dibujamos el rectángulo del bounds
            cv2.rectangle(frame, (xa+x, ya+y), (xa+x + w, ya+y + h), (0, 255, 0), 2)
            yellow_objects.append([xa+x+w/2 , ya+y+h/2])
            cv2.putText(frame,"YELLLOW color",(xa+x,ya+y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
            


    #Tracking the purple Color
    contornosimg = purple.copy()
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if (cv2.contourArea(c) < 200):
            continue
        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        elif(cv2.contourArea(c) > 5000):
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(c)
            # Dibujamos el rectángulo del bounds
            cv2.rectangle(frame, (xa+x, ya+y), (xa+x + w, ya+y + h), (255,0,255),2)
            purple_objects.append([xa+x+w/2 , ya+y+h/2])
            cv2.putText(frame,"purple color",(xa+x,ya+y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
    
          

    #Tracking the green Color
    
    contornosimg = green.copy()
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if (cv2.contourArea(c) < 200):
            continue
        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        elif(cv2.contourArea(c) > 5000):
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(c)
            # Dibujamos el rectángulo del bounds
            cv2.rectangle(frame, (xa+x, ya+y), (xa+x + w, ya+y + h), (255,0,255),2)
            green_objects.append([xa+x+w/2 , ya+y+h/2])
            cv2.putText(frame,"green color",(xa+x,ya+y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
    
            

    #Tracking the black Color
    
    contornosimg = black.copy()
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if (cv2.contourArea(c) < 200):
            continue
        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        elif(cv2.contourArea(c) > 5000):
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(c)
            # Dibujamos el rectángulo del bounds
            cv2.rectangle(frame, (xa+x, ya+y), (xa+x + w, ya+y + h), (255,0,255),2)
            black_objects.append([xa+x+w/2 , ya+y+h/2])
            cv2.putText(frame,"black color",(xa+x,ya+y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
    
             

    #Tracking the orange Color
    
    contornosimg = orange.copy()
    im, contornos, hierarchy = cv2.findContours(contornosimg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for c in contornos:
        # Eliminamos los contornos más pequeños
        if (cv2.contourArea(c) < 200):
            continue
        # Obtenemos el bounds del contorno, el rectángulo mayor que engloba al contorno
        elif(cv2.contourArea(c) > 5000):
            continue
        else:
            (x, y, w, h) = cv2.boundingRect(c)
            # Dibujamos el rectángulo del bounds
            cv2.rectangle(frame, (xa+x, ya+y), (xa+x + w, ya+y + h), (255,0,255),2)
            orange_objects.append([xa+x+w/2 , ya+y+h/2])
            cv2.putText(frame,"orange color",(xa+x,ya+y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
    
    
   if red_objects:
        finger_position_list[0].append(red_objects[0][0])
        finger_position_list[1].append(red_objects[0][1])
    else:
        finger_position_list[0].append(0)
        finger_position_list[1].append(0)

    if blue_objects:
        finger_position_list[0].append(blue_objects[0][0])
        finger_position_list[1].append(blue_objects[0][1])
    else:
        finger_position_list[0].append(0)
        finger_position_list[1].append(0)

    if yellow_objects:
        finger_position_list[0].append(yellow_objects[0][0])
        finger_position_list[1].append(yellow_objects[0][1])
    else:
        finger_position_list[0].append(0)
        finger_position_list[1].append(0)

    if green_objects:
        finger_position_list[0].append(green_objects[0][0])
        finger_position_list[1].append(green_objects[0][1])
    else:
        finger_position_list[0].append(0)
        finger_position_list[1].append(0)

    if purple_objects:
        finger_position_list[0].append(purple_objects[0][0])
        finger_position_list[1].append(purple_objects[0][1])
    else:
        finger_position_list[0].append(0)
        finger_position_list[1].append(0)

    if orange_objects:
        finger_position_list[0].append(orange_objects[0][0])
        finger_position_list[1].append(orange_objects[0][1])
    else:
        finger_position_list[0].append(0)
        finger_position_list[1].append(0)

    if black_objects:
        finger_position_list[0].append(black_objects[0][0])
        finger_position_list[1].append(black_objects[0][1])
    else:
        finger_position_list[0].append(0)
        finger_position_list[1].append(0)

    #print(a)
    dev = 1
    if (dev == 0):
        print(string(finger_position_list[0]), string(finger_position_list[1]))
    else:
        if finger_position_list[0] != [] and finger_position_list[1] !=[]:
            try:
                final_sentence = comparate_with_database(finger_position_list[0], finger_position_list[1])
                #send(final_sentence)
                print(final_sentence)
            except:
                print("Error")
                pass
            

    finger_position_list = [[], []]
    
    cv2.imshow("Color Tracking",frame)
    #cv2.frameshow("red",res)
    #cv2.imshow("Color", img3)

    k = cv2.waitKey(10)
    if k == 27:
        break
    

cap.release()
cv2.destroyAllWindows()
    
    