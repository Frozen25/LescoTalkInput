import cv2
import numpy as np
import math


cap = cv2.VideoCapture(0)
while(cap.isOpened()):
    # read image
    ret, img = cap.read()

    # get hand data from the rectangle sub window on the screen
    cv2.rectangle(img, (300,300), (100,100), (0,255,0),0)
    crop_img = img[100:300, 100:300]

    # convert to grayscale
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # applying gaussian blur
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)

    # thresholdin: Otsu's Binarization method
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # show thresholded image
    cv2.imshow('Thresholded', thresh1)

    # check OpenCV version to avoid unpacking error
    (version, _, _) = cv2.__version__.split('.')

    if version == '3':
        image, contours, hierarchy = cv2.findContours(thresh1.copy(), \
               cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    elif version == '2':
        contours, hierarchy = cv2.findContours(thresh1.copy(),cv2.RETR_TREE, \
               cv2.CHAIN_APPROX_NONE)

    # find contour with max area
    cnt = max(contours, key = lambda x: cv2.contourArea(x))

    # create bounding rectangle around the contour (can skip below two lines)
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x+w, y+h), (0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt)

    # drawing contours
    drawing = np.zeros(crop_img.shape,np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0,(0, 0, 255), 0)

    # finding convex hull
    hull = cv2.convexHull(cnt, returnPoints=False)

    # finding convexity defects
    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    # applying Cosine Rule to find angle for all defects (between fingers)
    # with angle > 90 degrees and ignore defects
    angulos = [0,0,0,0,0,0]

    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]

        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        # find length of all sides of triangle
        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        # apply cosine rule here
        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57

        # ignore angles > 90 and highlight rest with red dots
        if angle <=110:
        	angulos[count_defects] = round(angle,1)
        	count_defects += 1
        	cv2.circle(crop_img, far, 1, [0,0,255], -1)
        #dist = cv2.pointPolygonTest(cnt,far,True)

        # draw a line from start to end i.e. the convex points (finger tips)
        # (can skip this part)
        cv2.line(crop_img,start, end, [0,255,0], 2)
        #cv2.circle(crop_img,far,5,[0,0,255],-1)

    print (angulos[:4])
    # define actions required
    if count_defects == 1:
        cv2.putText(img,"I am Vipul", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    elif count_defects == 2:
        str = "This is a basic hand gesture recognizer"
        cv2.putText(img, str, (5, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
    elif count_defects == 3:
        cv2.putText(img,"This is 4 :P", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    elif count_defects == 4:
        cv2.putText(img,"Hi!!!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    else:
        cv2.putText(img,"Hello World!!!", (50, 50),\
                    cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

    # show appropriate images in windows
    cv2.imshow('Gesture', img)
    all_img = np.hstack((drawing, crop_img))
    cv2.imshow('Contours', all_img)

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

	#defining the range of purple color
    purple_lower=np.array([110,100,100],np.uint8)
    purple_upper=np.array([130,255,255],np.uint8)

    #defining the range of green color
    green_lower=np.array([34,50,50],np.uint8)
    green_upper=np.array([80,200,200],np.uint8)

    #defining the range of black color
    black_lower=np.array([0,0,0],np.uint8)
    black_upper=np.array([255,50,50],np.uint8)

    #defining the range of oragen color
    orange_lower=np.array([10,100,100],np.uint8)
    orange_upper=np.array([15,255,255],np.uint8)

    #finding the range of red,blue and yellow color in the image
    red=cv2.inRange(hsv,red_lower,red_upper)
    blue=cv2.inRange(hsv,blue_lower,blue_upper)
    yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)
    purple=cv2.inRange(hsv,purple_lower,purple_upper)
    green=cv2.inRange(hsv,green_lower,green_upper)
    black=cv2.inRange(hsv,black_lower,black_upper)
    orange=cv2.inRange(hsv,orange_lower,orange_upper)

    #Morphological transformation, Dillation
    kernal = np.ones((5,5),"uint8")

    red=cv2.dilate(red,kernal)
    Rres=cv2.bitwise_and(img2, img2, mask=red)

    blue=cv2.dilate(blue,kernal)
    Bres=cv2.bitwise_and(img2, img2, mask=blue)

    yellow=cv2.dilate(yellow,kernal)
    Yres=cv2.bitwise_and(img2, img2, mask=yellow)

    purple=cv2.dilate(purple,kernal)
    Pres=cv2.bitwise_and(img2, img2, mask=purple)

    green=cv2.dilate(green,kernal)
    Gres=cv2.bitwise_and(img2, img2, mask=green)

    black=cv2.dilate(black,kernal)
    blackres=cv2.bitwise_and(img2, img2, mask=black)

    orange=cv2.dilate(orange,kernal)
    Ores=cv2.bitwise_and(img2,img2, mask = orange)

    #Tracking the Red Color
    (_,contours, hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x,y,w,h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img2,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255))

    #Tracking the Blue Color
    (_,contours, hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x,y,w,h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img2,"BLUE color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0))

    #Tracking the YELLOW Color
    (_,contours, hierarchy)=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x,y,w,h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.putText(img2,"YELLLOW color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))

    #Tracking the purple Color
    (_,contours, hierarchy)=cv2.findContours(purple,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x,y,w,h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(255,0,255),2)
            cv2.putText(img2,"purple color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))



    #Tracking the green Color
    (_,contours, hierarchy)=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x,y,w,h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(255,0,255),2)
            cv2.putText(img2,"green color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))


    #Tracking the black Color
    (_,contours, hierarchy)=cv2.findContours(black,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x,y,w,h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(255,0,255),2)
            cv2.putText(img2,"black color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))

    #Tracking the orange Color
    (_,contours, hierarchy)=cv2.findContours(orange,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for pic,contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 200):
            x,y,w,h = cv2.boundingRect(contour)
            img2 = cv2.rectangle(img2,(x,y),(x+w,y+h),(255,0,255),2)
            cv2.putText(img2,"orange color",(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))


    #cv2.img2show("Redcolour",red)
    cv2.imshow("Color Tracking",img2)
    #cv2.img2show("red",res)

    k = cv2.waitKey(10)
    if k == 27:
        break
