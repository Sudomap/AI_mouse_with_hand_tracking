import cv2
import mediapipe as mp
import time
import mouse



class handDetector():
    def __init__(self, mode=False, max_hands=2, min_detect_conf=0.5, min_track_conf=0.5):
        self.mode = mode
        self.maxHands = max_hands
        self.detectConf = min_detect_conf
        self.trackConf = min_track_conf
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(frame, handLms, self.mpHands.HAND_CONNECTIONS)
        return frame

    def findPosition(self, frame, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                # return cx, cy

                #if id == 8:
                    #print(id, cx, cy)
                    #if draw:
                        #cv2.circle(frame, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
                    #mouse.move(cy, cy)
                #if id == 4:
                    #print(id, cx, cy)
                    #if draw:
                        #cv2.circle(frame, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
                    #mouse.move(cy, cy)
        return lmList





def Main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam")
    detector = handDetector()
    while True:
        ret, frame = cap.read()
        frame = detector.findHands(frame)
        lmList = detector.findPosition(frame)
        if len(lmList) != 0:
            print(f"{lmList[8]}")
        else:
            print("No hand")
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 2)

        cv2.imshow('handtrack', frame)
        if cv2.waitKey(10) == ord("q"):
            break

if __name__ == '__main__':
    Main()