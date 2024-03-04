import cv2 as cv #a library in python to capture image.
import mediapipe as mp 
import math
import numpy


from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

 
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)













mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv.VideoCapture(0)

while True:
    success,img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    #detected palm
    results = hands.process(imgRGB)
    #if palm is detected.
    if results.multi_hand_landmarks:
        #loop through all the hands.
        for handlms in results.multi_hand_landmarks:
            lmlist=[]
            for id,lm in enumerate(handlms.landmark):
                h, w, c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                lmlist.append([id,cx,cy])
                #print(id,ln)
                #mp_drawing.draw_landmarks(img,handlms, mp_hands.HAND_CONNECTIONS)
            if lmlist:
                #CO-ORDINATES OF THUMBS AND FORE FINGER.
                x1,y1 = lmlist[4][1], lmlist[4][2]
                x2,y2 = lmlist[8][1], lmlist[8][2]
                #circle around thumb 
                cv.circle(img,(x1,y1), 15, (1,23,123), cv.FILLED)
                #circle around forefinger.
                cv.circle(img,(x2,y2), 15, (1,23,123), cv.FILLED)
                #line between two tips.
                cv.line(img, (x1,y1), (x2,y2), (1,23,123), 4)
                z1 ,z2 = (x1+x2)//2 , (y1+y2)//2
                length = math.hypot(x2-x1, y2-y1)
                print(length)
            volRange = volume.GetVolumeRange() 
            minvol = volRange[0]
            maxvol = volRange[1]
            vol = numpy.interp(length,[50,100],[minvol, maxvol])
            volPer = numpy.interp(length,[50,100],[0,100])
            volBar = numpy.interp(length ,[50,100], [400,150])



            volume.SetMasterVolumeLevel(vol, None)
            cv.putText(img,str(int(volPer)),(40,450),cv.FONT_HERSHEY_COMPLEX, 5 , (1,3,5),3)
            cv.rectangle(img,(50,150),(85,400),(123,213,122),3)
            cv.rectangle(img, (50,int(volBar)),(85,400), (0 ,231 ,23), cv.FILLED)

    cv.imshow("Image",img)
    cv.waitKey(1)
