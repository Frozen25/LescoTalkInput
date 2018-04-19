import cv2
import numpy as np
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

while (cap.isOpened()):
    _, img2 = cap.read()

    # converting frame (img2 i.e BGR) to HSV (hue-saturation-value)

    hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)

    # defining the range of red color
    red_lower = np.array([170, 100, 100], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    # defining the range of blue color
    blue_lower = np.array([99, 100, 100], np.uint8)
    blue_upper = np.array([110, 255, 255], np.uint8)

    # defining the range of yellow color
    yellow_lower = np.array([20, 100, 100], np.uint8)
    yellow_upper = np.array([30, 255, 255], np.uint8)

    # defining the range of purple color
    purple_lower = np.array([124, 18, 91], np.uint8)
    purple_upper = np.array([152, 45, 140], np.uint8)

    # defining the range of green color
    green_lower = np.array([78, 100, 100], np.uint8)
    green_upper = np.array([96, 200, 200], np.uint8)

    # defining the range of black color
    black_lower = np.array([0, 0, 0], np.uint8)
    black_upper = np.array([120, 60, 61], np.uint8)

    # defining the range of oragen color
    orange_lower = np.array([8, 90, 96], np.uint8)
    orange_upper = np.array([18, 150, 225], np.uint8)

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
    #cv2.putText(img2, 'hola', (100, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv2.imshow("Color Tracking", img2)
    #cv2.imshow("Color", img3)

    k = cv2.waitKey(10)
    if k == 27:
        break
