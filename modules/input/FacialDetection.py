from ..abstract.InputAbstract import InputAbstractClass
import numpy as np
import cv2

import importlib
#stasm_spec = importlib.util.find_spec("stasm")
stasm_spec = importlib.find_loader("stasm")
found = stasm_spec is not None

if found:
    import stasm

from PIL import Image

class FacialDetection(InputAbstractClass):

    def convertArrayToNumpy(self, pts):
        ptsNp = np.array(pts, np.int32)
        ptsNp = ptsNp.reshape((-1,1,2))
        return ptsNp

    def recogniseActions(self, img, pts):

        #Clear actions
        for key in self.actions.keys():
            self.actions[key] = False


        # Nose Position
        nose  = self.convertArrayToNumpy(
                    pts[self.Face["NoseNostrils"][0]:self.Face["NoseNostrils"][-1]])

        pointX = [nose[4]][0][0][0]
        pointY = [nose[4]][0][0][1]


        if (pointX > self.deadZoneRight):
            self.actions["Right"] = True
        elif (pointX < self.deadZoneLeft):
            self.actions["Left"] = True

        if (pointY > self.deadZoneDown):
            self.actions["Down"] = True
        elif (pointY < self.deadZoneUp):
            self.actions["Up"] = True
        # Mouth actions
        # top 68, bottom 69
        # ptsUpperLip = convertArrayToNumpy(pts[Face["UpperLip"][0]:Face["UpperLip"][-1]])
        # ptsLowerLip = convertArrayToNumpy(pts[Face["LowerLip"][0]:Face["LowerLip"][-1]])

        ptsUpperLip = [self.convertArrayToNumpy(pts[68])][0][0][0][1]
        ptsLowerLip = [self.convertArrayToNumpy(pts[69])][0][0][0][1]

        diff = abs(ptsUpperLip - ptsLowerLip)
        gap = 10

        if (diff > gap):
            self.actions["MouthOpen"] = True


    def drawOutlines(self, img, pts, color):
        for k in self.Face.keys():
            ptsNp = self.convertArrayToNumpy(pts[self.Face[k][0]:self.Face[k][-1]])
            cv2.polylines(img, [ptsNp], True, color)

        return img

    def paintDaFaceBro(self, img, pts):

        #Face Outline
        ptsEye1= pts[self.Face["LeftPupil"][0]]
        ptsEye2 = pts[self.Face["RightPupil"][0]]
        # cv2.line(img, tuple(ptsEye1), tuple(ptsEye2), (0,0,255), 3)
        # cv2.circle(img, tuple(ptsNp), 3, (0,0,255), -1)

        return self.drawOutlines(img, pts, (0,255,0))

    def paintDebugLines(self, img, pts):

        nose  = self.convertArrayToNumpy(
                    pts[self.Face["NoseNostrils"][0]:self.Face["NoseNostrils"][-1]])

        pointX = [nose[4]][0][0][0]
        pointY = [nose[4]][0][0][1]

        colour = (255, 255, 255)
        strokeWidth = 1
        deadZoneColour = (255, 0, 0)


        cv2.line(img, (pointX,0), (pointX, self.height), colour, strokeWidth)
        cv2.line(img, (0, pointY), (self.width, pointY), colour, strokeWidth)

        cv2.line(img, (self.deadZoneLeft,0), (self.deadZoneLeft, self.height), deadZoneColour, strokeWidth)
        cv2.line(img, (self.deadZoneRight,0), (self.deadZoneRight, self.height), deadZoneColour, strokeWidth)

        cv2.line(img, (0,self.deadZoneUp), (self.width,self.deadZoneUp), deadZoneColour, strokeWidth)
        cv2.line(img, (0,self.deadZoneDown), (self.width,self.deadZoneDown), deadZoneColour, strokeWidth)

        return img

    def displayActions(self, img):
        count = 0
        x = 460
        y = 60
        dy = 30

        cv2.putText(img,"Actions:", (x,y), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 1)

        for key, value in self.actions.items():
            if (value):
                count += 1
                cv2.putText(img, str(key), (x,y + (dy*count)), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (255, 0, 255), 1)
        return img

    def init(self):
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

        self.paintDebug = False

        # Define actions here
        self.actions = {
            "MouthOpen": False,
            "Left": False,
            "Right": False,
            "Up": False,
            "Down": False
        }

        self.window = None

        self.deadZoneLeft = 0
        self.deadZoneRight = 0
        self.deadZoneUp = 0
        self.deadZoneDown = 0

        self.width = 0
        self.height = 0

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


                # for i in range(0, len(pts)):
                #     # print("i: ",i, " - ", pts[i][0], " , ", pts[i][1])
                #     # cv2.putText(frame, str(i), (pts[i][0], pts[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0,255,0), 1, cv2.LINE_AA)

                #     # frame[int(round(point[1]))][int(round(point[0]))] = (0,255,0)
                #     continue

            # Image is ready for use
            # cv2.imshow("STASM", frame)

    def getData(self):
        # print ("Facial get data!")
        return self.landmarks
        # return self.actions

    def display(self, window):

        self.window = window

        if (not self.face_found and self.ret):
            window.print("No face found")
        
        if (self.frame is not None):
            # print (type(self.frame))
            # window.update_image(np.array(self.frame))
            self.frame = self.frame[...,::-1]
            image = Image.fromarray(self.frame)
            # image.save("test.jpg")

            window.update_image(image)
        # pass

    def keyboard(self, key):
        # self.window.print("Got key in face rec: " + key)
        if (key == 'd'):
            self.paintDebug = not self.paintDebug
            self.window.print("Debug mode now: " + str(self.paintDebug))

    def mouse_click(self, x, y):
        pass
        
