import cv2
import numpy as np
from csv_managment import comparate_with_database
import socket

adress = '0.0.0.0'
port = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((adress, port))
sock.listen(1)

connections = []
withAndroid = 0

finger_position_list = [[], []]

counter = 0
salidaFinal = ""
isSend = False
mensaje = ""


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
        send("hola")
        break

    print("Connected")
    print(connections)

cap = cv2.VideoCapture(0)


muestras = 0
vecmin , vecmax = [999,999,999] , [0,0,0]
mousex , mousey = -1,-1


def mouseclic(event,x,y,flags,param):
    global muestras , vecmax , vecmin
    if event == cv2.EVENT_LBUTTONUP:
        pixelbrg = img3[y,x]
        pixelnp = np.uint8([ [ pixelbrg ] ] )
        pixelhsv = cv2.cvtColor(pixelnp,cv2.COLOR_BGR2HSV)
        pixelvec = pixelhsv[0][0]
        if (pixelvec[0] > vecmax[0]):
            vecmax[0] = pixelvec[0] 
        if (pixelvec[1] > vecmax[1]):
            vecmax[1] = pixelvec[1] 
        if (pixelvec[2] > vecmax[2]):
            vecmax[2] = pixelvec[2] 
        if (pixelvec[0] < vecmin[0]):
            vecmin[0] = pixelvec[0] 
        if (pixelvec[1] < vecmin[1]):
            vecmin[1] = pixelvec[1] 
        if (pixelvec[2] < vecmin[2]):
            vecmin[2] = pixelvec[2] 
        muestras +=1



_, img3 = cap.read()


red_lower, red_upper , blue_lower , blue_upper, green_lower , green_upper , purple_lower, purple_upper 
    yellow_lower , yellow_upper , orange_lower , orange_upper , black_lower , black_upper = 0,0,0,0,0,0,0,0,0,0,0,0,0,0

while (cap.isOpened()):
    cv2.imshow("Calibration", img3)
    cv2.setMouseCallback('Calibration',mouseclic)

    if muestras == 5:
        blue_lower = np.array(vecmin, np.uint8)
        blue_upper = np.array(vecmax, np.uint8)
        vecmin = [999,999,999] 
        vecmax = [0,0,0]
    if muestras == 15:
        purple_lower = np.array(vecmin, np.uint8)
        purple_upper = np.array(vecmax, np.uint8)
        vecmin = [999,999,999] 
        vecmax = [0,0,0]
    if muestras == 15:
        red_lower = np.array(vecmin, np.uint8)
        red_upper = np.array(vecmax, np.uint8)
        vecmin = [999,999,999] 
        vecmax = [0,0,0]
    if muestras == 20:
        green_lower = np.array(vecmin, np.uint8)
        green_upper = np.array(vecmax, np.uint8)
        vecmin = [999,999,999] 
        vecmax = [0,0,0]
    if muestras == 25:
        yellow_lower = np.array(vecmin, np.uint8)
        yellow_upper = np.array(vecmax, np.uint8)
        vecmin = [999,999,999] 
        vecmax = [0,0,0]
    if muestras == 30:
        black_lower = np.array(vecmin, np.uint8)
        black_upper = np.array(vecmax, np.uint8)
        vecmin = [999,999,999] 
        vecmax = [0,0,0]
    
    
    
    
    



    k = cv2.waitKey(10)
    if k == 8:
        break
    
_, img3 = cap.read()

while (cap.isOpened()):
    cv2.imshow("Calibration", img3)
    cv2.setMouseCallback('Calibration',mouseclic)
    
    if muestras == 35:
        orange_lower = np.array(vecmin, np.uint8)
        orange_upper = np.array(vecmax, np.uint8)
        vecmin = [999,999,999] 
        vecmax = [0,0,0]

    k = cv2.waitKey(10)
    if k == 8:
        break



while (cap.isOpened()):
    _, img2 = cap.read()

    # converting frame (img2 i.e BGR) to HSV (hue-saturation-value)

    hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

    '''
        # defining the range of red color
    red_lower = np.array([175, 130, 51], np.uint8)
    red_upper = np.array([180, 180, 100], np.uint8)

    # defining the range of blue color
    blue_lower = np.array([99, 100, 100], np.uint8)
    blue_upper = np.array([110, 255, 255], np.uint8)

    # defining the range of yellow color
    yellow_lower = np.array([15, 130, 88], np.uint8)
    yellow_upper = np.array([28, 210, 165], np.uint8)

    # defining the range of purple color
    purple_lower = np.array([165, 100, 51], np.uint8)
    purple_upper = np.array([175, 130, 81], np.uint8)

    # defining the range of green color
    green_lower = np.array([80, 100, 50], np.uint8)
    green_upper = np.array([95, 130, 90], np.uint8)

    # defining the range of black color
    black_lower = np.array([0, 0, 0], np.uint8)
    black_upper = np.array([250, 50, 40], np.uint8)

    # defining the range of oragen color
    orange_lower = np.array([3, 130, 120], np.uint8)
    orange_upper = np.array([15, 170, 160], np.uint8)
    '''

    # finding the range of red,blue and yellow color in the image
    red = cv2.inRange(hsv, red_lower, red_upper)
    blue = cv2.inRange(hsv, blue_lower, blue_upper)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    purple = cv2.inRange(hsv, purple_lower, purple_upper)
    green = cv2.inRange(hsv, green_lower, green_upper)
    black = cv2.inRange(hsv, black_lower, black_upper)
    orange = cv2.inRange(hsv, orange_lower, orange_upper)

    # Morphological transformation, Dillation
    kernal = np.ones((5, 5), "uint8")

    red = cv2.dilate(red, kernal)
    Rres = cv2.bitwise_and(img2, img2, mask=red)

    blue = cv2.dilate(blue, kernal)
    Bres = cv2.bitwise_and(img2, img2, mask=blue)

    yellow = cv2.dilate(yellow, kernal)
    Yres = cv2.bitwise_and(img2, img2, mask=yellow)

    purple = cv2.dilate(purple, kernal)
    Pres = cv2.bitwise_and(img2, img2, mask=purple)

    green = cv2.dilate(green, kernal)
    Gres = cv2.bitwise_and(img2, img2, mask=green)

    black = cv2.dilate(black, kernal)
    blackres = cv2.bitwise_and(img2, img2, mask=black)

    orange = cv2.dilate(orange, kernal)
    Ores = cv2.bitwise_and(img2, img2, mask=orange)

    red_objects, blue_objects, yellow_objects, green_objects, orange_objects, purple_objects, black_objects = [], [], [], [], [], [], []

    # Tracking the Red Color
    contador = 0
    (_, contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x, y, w, h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
            red_objects.append([x + w / 2, y + h / 2])
            cv2.putText(img2, "RED", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))

    # Tracking the Blue Color
    contador = 0
    (_, contours, hierarchy) = cv2.findContours(blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x, y, w, h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
            blue_objects.append([x + w / 2, y + h / 2])
            cv2.putText(img2, "BLUE", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0))

    # Tracking the YELLOW Color
    contador = 0
    (_, contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x, y, w, h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 0, 255), 2)
            yellow_objects.append([x + w / 2, y + h / 2])
            cv2.putText(img2, "YELLLOW", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))

    # Tracking the purple Color
    contador = 0
    (_, contours, hierarchy) = cv2.findContours(purple, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x, y, w, h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 255), 2)
            purple_objects.append([x + w / 2, y + h / 2])
            cv2.putText(img2, "PURṔLE", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))

    # Tracking the green Color
    contador = 0
    (_, contours, hierarchy) = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x, y, w, h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 255), 2)
            green_objects.append([x + w / 2, y + h / 2])
            cv2.putText(img2, "GREEN", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))

    # Tracking the black Color
    contador = 0
    (_, contours, hierarchy) = cv2.findContours(black, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x, y, w, h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 255), 2)
            black_objects.append([x + w / 2, y + h / 2])
            cv2.putText(img2, "BLACK", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))

    # Tracking the orange Color
    contador = 0
    (_, contours, hierarchy) = cv2.findContours(orange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x, y, w, h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2, (x, y), (x + w, y + h), (255, 0, 255), 2)
            orange_objects.append([x + w / 2, y + h / 2])
            cv2.putText(img2, "ORANGE", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0))

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

    dev = 1
    if (dev == 0):
        print(string(finger_position_list[0]), string(finger_position_list[1]))
    else:
        if finger_position_list[0] != [] and finger_position_list[1] !=[]:
            try:
                final_sentence = comparate_with_database(finger_position_list[0], finger_position_list[1])
                if(final_sentence == ""):
                    pass
                elif(final_sentence == "*"):
                    counter=0
                    if (mensaje != ""):
                        #send(mensaje)
                        print("Mensaje es ", mensaje)
                        mensaje = ""
                elif(final_sentence == salidaFinal):
                    print(final_sentence)
                    if(counter >= 10):
                        print (counter)
                        if(not isSend):
                            mensaje= mensaje + final_sentence
                            final_sentence = ""
                            isSend= True
                            counter+=1
                            print(mensaje)
                        else:
                            counter+=1
                    else:
                        print (counter)
                        counter+=1
                        print(final_sentence)
                else:
                    salidaFinal = final_sentence
                    counter=0
                    isSend=False


            except:
                print("Error")
                pass

            

    finger_position_list = [[], []]
    #cv2.putText(img2, 'hola', (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    
    cv2.imshow("Color Tracking", img2)
    

    k = cv2.waitKey(10)
    if k == 27:
        break
