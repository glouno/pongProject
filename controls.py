# Here we'll use the opencv module to send the control inputs to the game
import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from matplotlib import pyplot as plt

liveVideo = cv.VideoCapture(0)
handDetector = HandDetector(detectionCon = 0.8, maxHands=2)


while True:
    ret, frame = liveVideo.read()
    frame = cv.flip(frame, 1)
    hands, frame = handDetector.findHands(frame, flipType=False)

    '''
    if hands.any():
        # bboxInfo - "id","bbox","score","center"
        center = hands[0]["center"]
        cv.circle(frame, center, 5, (255, 0, 255), cv.FILLED)
    '''

    #HAND DETECTION
    #Use element number 8: INDEX_FINGER_TIP

    #for each hand we'Ll have info Like Hand--›dict{lmList,boundinqboundary, img)
    if hands:
        hand1=hands[0]                          #gives us first hand
        lmList1=hand1["lmList"]                 #List of 21 Landmarks
        bbox1=hand1["bbox"]                     #x,y,w,h of bounding box
        centerPoint1=hand1[ "center" ]          #center of the hand cx, cy
        handType1=hand1["type"]                #Left or right
        finger1=handDetector.fingersUp(hand1)
        
        #needs something to find the distance / x,y positions 
        #length, info, frame=handDetector.findDistance(lmList1[8], lmList1[12])

    if len(hands)==2:
        hand2=hands[1]                          #gives us second hand
        lmList2=hand2["lmList"]                 #List of 21 Landmarks
        bbox2=hand2["bbox" ]                    #x,y, w,h of bounding box
        centerPoint2=hand2["center"]            #center of the hand cx, cy
        handType2=hand2["type" ]                #Left or right
        finger2=handDetector.fingersUp(hand2)
        #length, info, frame=handDetector.findDistance(lmList1[8],lmList2[8],frame)
        #length, info, frame=handDetector.findDistance(centerPoint1, centerPoint2, frame)


    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
liveVideo.release()
# Destroy all the windows
cv.destroyAllWindows()

