from ..abstract.ClassifierAbstract import ClassifierAbstractClass

import numpy as np

class FaceClassifier(ClassifierAbstractClass):

    def init(self):
        # print ("Face classifier init!")
        self.window = None
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

        self.deadZones = None
        self.actions = {
            "MouthOpen": False,
            "Left": False,
            "Right": False,
            "Up": False,
            "Down": False
        }
        #,data

    def classify_point_data(self, pts):
        if (len(pts) == 0):
            return

        #Clear actions
        for key in self.actions.keys():
            self.actions[key] = False

        # Nose Position
        nose  = self.convertArrayToNumpy(
                    pts[self.Face["NoseNostrils"][0]:self.Face["NoseNostrils"][-1]])
        
        # print(nose)
        # print(pts)

        pointX = [nose[4]][0][0][0]
        pointY = [nose[4]][0][0][1]

        if (pointX > self.deadZones["deadZoneRight"]):
            self.actions["Right"] = True
        elif (pointX < self.deadZones["deadZoneLeft"]):
            self.actions["Left"] = True

        if (pointY > self.deadZones["deadZoneDown"]):
            self.actions["Down"] = True
        elif (pointY < self.deadZones["deadZoneUp"]):
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
    def update(self, data):

        pts, img = data
        self.classify_point_data(pts)

    def getAction(self):
        # print ("Face classifier action")
        return self.actions

    def display(self, window):
        pass

    def keyboard(self, key):
        pass

    def mouse_click(self, x, y):
        pass

    def set_params(self, params):
        if (self.deadZones is None):
            self.deadZones = params

    def convertArrayToNumpy(self, pts):
        ptsNp = np.array(pts, np.int32)
        ptsNp = ptsNp.reshape((-1,1,2))
        return ptsNp