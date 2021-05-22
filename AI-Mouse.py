import cv2
import mediapipe as mp
import time
import mouse
import HandTrackingModual as htm
import math
import numpy as np

##############################
# For the FPS
pTime = 0
cTime = 0
##############################
cap = cv2.VideoCapture('Handvid.mp4')
##############################
# Change this to your monitor's screen size
width = 1600
height = 900
dim = (width, height)
##############################
# For smoothening the mouse movement
smoothening = 5
plocx, plocy = 0, 0
clocx, clocy = 0, 0
##############################
# To prevent to much clicking
mouseClicked = False
##############################
if not cap.isOpened():
    print("Could not open webcam")
detector = htm.handDetector(max_hands=1, min_detect_conf=0.6, min_track_conf=0.4)
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)
    lmList = detector.findPosition(frame)
    if len(lmList) != 0:
        print(f"{lmList[8]}")
        clocx = plocx + (lmList[9][1] - plocx) / smoothening
        clocy = plocy + (lmList[9][2] - plocy) / smoothening
        mouse.move(clocx, clocy)
        plocx, plocy = clocx, clocy
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[6][1], lmList[6][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        cv2.circle(frame, (x1, y1), 15, (155, 234, 54), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 15, (155, 234, 54), cv2.FILLED)
        cv2.circle(frame, (cx, cy), 15, (155, 234, 54), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (155, 234, 54), 3)
        length = math.hypot(x2 - x1, y2 - y1)
        print(length)
        # If the index finger is up, don't click, if it's down, click once. However, what if you want to click and drag? Move the thumb over to the palm.
        # Remember, I'm kind of new to Python, so not all of it will work.
        if lmList[8][2] > lmList[6][2]:
            if not mouseClicked:
                mouse.click()
                cv2.circle(frame, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                print("Mouse click")
                mouseClicked = True
            elif lmList[4][1] > lmList[6][1]:
                mouse.click()
                cv2.circle(frame, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
                print("Mouse click")
        else:
            mouseClicked = False

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 2)

    cv2.imshow('handtrack', frame)
    if cv2.waitKey(10) == ord("q"):
        break
