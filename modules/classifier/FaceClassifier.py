from ..abstract.ClassifierAbstract import ClassifierAbstractClass

# Neural Network required libraries
import numpy as np
import mxnet as mx
import onnx_mxnet
import cv2
from collections import namedtuple
from PIL import Image

import time

_SIZE = 350
_DEAD_TIME = 0.5

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
            "Down": False,
        }

        # this won't fail if you give it the wrong file path :/
        self.faceCascade = cv2.CascadeClassifier("support_programs/haarcascade_frontalface_default.xml")

        self.sym, self.arg = onnx_mxnet.import_model('support_programs/NN_V03_01.onnx')

        test_image = np.zeros((350,350))
        # (1, 1, 350, 350)
        # (480, 640, 3)

        self.data_names = [graph_input for graph_input in self.sym.list_inputs()
                    if graph_input not in self.arg]

        self.mod = mx.mod.Module(symbol=self.sym, data_names=self.data_names, context=mx.cpu(), label_names=None)
        self.mod.bind(for_training=False, data_shapes=[(self.data_names[0], test_image.shape)], label_shapes=None)
        self.mod.set_params(arg_params=self.arg, aux_params=self.arg, allow_missing=True, allow_extra=True)

        self.Batch = namedtuple('Batch', ['data'])
        self.output_labels = ["anger", "neutral", "scream", "smile"]
        
        self.nn_results = {}

        self.start = time.clock()
        # print(self.start)
        # print(test_image.shape)
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

    # Returns only the face in the correct format
    def chop_face(self, frame):
        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # print(frame)

        faces = self.faceCascade.detectMultiScale(frame,
                                                scaleFactor=1.2,
                                                minNeighbors=8,
                                                minSize=(50,50),
                                                flags=cv2.CASCADE_SCALE_IMAGE
                                                )

        # print("Got a face?")
        for (x, y, w, h) in faces:
            # Get original size of face
            # print("Do I make it here?")
            img = frame[y:(y+h), x:(x+w)]
            return np.asarray(Image.fromarray(img).resize((_SIZE, _SIZE)))
        return None

    def classify_neural_network(self, img):
        img = self.chop_face(img)

        # print("here?")
        if (img is not None):
            try:
                # print(img.shape)
                self.mod.forward(self.Batch([mx.nd.array(img)]))
            except:
                print("something failed")
            # print("output time?")
            output = self.mod.get_outputs()[0][0].asnumpy().tolist()
            self.nn_results = dict(zip(self.output_labels, output))
            # for key, value in self.nn_results.items():
            #     print(key + ":" + str(value))


    def update(self, data):

        pts, img = data
        if (len(pts) > 0):
            self.classify_point_data(pts)
        if (len(img) > 0 and (time.clock() - self.start > _DEAD_TIME)):
            self.classify_neural_network(img)
            self.start = time.clock()

    def getAction(self):
        # print ("Face classifier action")
        return [self.actions, self.nn_results]

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