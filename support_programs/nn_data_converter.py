import numpy as np
import cv2

### UNFINISHED ### 

import importlib
#stasm_spec = importlib.util.find_spec("stasm")
stasm_spec = importlib.find_loader("stasm")
found = stasm_spec is not None

if found:
    import stasm

from PIL import Image

class FacialDetection():

    def convertArrayToNumpy(self, pts):
        ptsNp = np.array(pts, np.int32)
        ptsNp = ptsNp.reshape((-1,1,2))
        return ptsNp


    def drawOutlines(self, img, pts, color):
        for k in self.Face.keys():
            ptsNp = self.convertArrayToNumpy(pts[self.Face[k][0]:self.Face[k][-1]])
            cv2.polylines(img, [ptsNp], True, color)

        return img

    def __init__(self):
        # need to convert list as it returns iterator
        # second number is exclusive
        self.Face = {
            "Outline":list(range(0, 16)),
            "LeftEyebrow" : list(range(16, 22)),
            "RightEyebrow" : list(range(22, 28)),
            "RightEyeTop" : [28],
            "LeftEyeTop" : [29],
            "LeftEye" : list(range(30,38)),
            "LeftPupil" : [38],
            "RightPupil" : [39],
            "RightEye" : list(range(40, 48)),
            #"NoseBridge" : list(range(48, 51)),
            "NoseNostrils" : list(range(48, 59)),
            "UpperLip" : list(range(59, 69)),
            "LowerLip" : list(range(69, 77)),
        }

        self.firstRun = True
        self.open_camera = False
        self.face_found = False

        self.landmarks = None

        # print ("Facial Detection!")
        try:
            # Set VideoCapture card number here (2 works on my machine)
            self.cap = cv2.VideoCapture(0)
            self.open_camera = False
        except:
            print ("Cannot open VideoCamera! Make sure you have the right one set in FacialDetection.py")

    def run(self):
        pass

    def update(self):
        self.ret, self.frame = self.cap.read()

        if self.ret == True and found:

            self.frame = cv2.flip(self.frame, 1)
            
            if (self.firstRun):
                segment = 16
                height = np.size(self.frame, 0)
                width = np.size(self.frame, 1)

                # print (height, "x", width)

                self.deadZoneLeft = int((width/2) - (width/segment))
                self.deadZoneRight = int((width/2) + (width/segment))

                self.deadZoneUp = int((height/2) - (height/segment))
                self.deadZoneDown = int((height/2) + (height/segment))

                self.firstRun = False

            #imgCol = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.img = cv2.cvtColor(self. frame, cv2.COLOR_BGR2GRAY)

            # do processing here
            self.landmarks = stasm.search_single(self.img)
            # print (len(landmarks))
            if len(self.landmarks) == 0:
                self.face_found = False
            else:
                self.landmarks = stasm.force_points_into_image(self.landmarks, self.img)
                self.face_found = True
                
                # print("Number of landmark points: ", len(landmarks))
                pts = []
                #pts = np.array(, np.int32)
                for point in self.landmarks:
                    pts.append([int(round(point[0])), int(round(point[1]))])
                #print(pts)
                ptsNp = np.array(pts, np.int32)
                #print (pts)
                ptsNp = ptsNp.reshape((-1,1,2))
                #cv2.polylines(frame, [ptsNp], False, (0,255,0))
                self.frame = self.paintDaFaceBro(self.frame, pts)
                if (self.paintDebug):
                    self.frame = self.paintDebugLines(self.frame, pts)
                
                self.recogniseActions(self.frame, pts)
                self.frame = self.displayActions(self.frame)


                for i in range(0, len(pts)):
                    # print("i: ",i, " - ", pts[i][0], " , ", pts[i][1])
                    # cv2.putText(frame, str(i), (pts[i][0], pts[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1, cv2.LINE_AA)

                    # frame[int(round(point[1]))][int(round(point[0]))] = (0,255,0)
                    continue