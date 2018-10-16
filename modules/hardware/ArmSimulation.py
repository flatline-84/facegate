from ..abstract.HardwareAbstract import HardwareAbstractClass

import matplotlib
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import mpl_toolkits.mplot3d.axes3d as p3
import math
import numpy as np
import re
import time
import tkinter as tk

# Get matplotlib to use TK
matplotlib.use("TkAgg")

class Drawing:
    def __init__(self, window):

        # self.fig = plt.figure()
        self.fig = Figure()

        self.ax = self.fig.add_subplot(111, projection='3d')


        self.ax.set_xlim(0, 200)
        self.ax.set_ylim(0, 200)
        self.ax.set_zlim(0, 200)
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')

        self.xCoordinates = np.array([])
        self.yCoordinates = np.array([])
        self.zCoordinates = np.array([])

        self.ax.set_axis_on()

        root = window.get_root()

        print("creating new Figure Canvas")
        canvas = FigureCanvasTkAgg(self.fig, root)
        canvas.get_tk_widget().grid(row=0, column=2, rowspan=2, sticky=tk.E)
        canvas.draw()
    def get_fig(self):
        return self.fig

class Arm:
    def __init__(self, points, bend_axis):

        self.points = points
        self.bend_axis = bend_axis

    def rotation_axis(self):
        x = self.points[1][0] - self.points[0][0]
        y = self.points[1][1] - self.points[0][1]
        z = self.points[1][2] - self.points[0][2]
        print("x=", x)
        print("y=", y)
        print("z=", z)
        mag = math.sqrt(x*x+y*y+z*z)
        print("mag=", mag)
        return [x/mag, y/mag, z/mag]

def create_rotation_matrix(u, theta):
    ux = u[0]
    uy = u[1]
    uz = u[2]
    rotation_matrix = [
        [math.cos(theta) + ux * ux * (1 - math.cos(theta)), ux * uy * (1 - math.cos(theta)) - uz * math.sin(theta),
         ux * uz * (1 - math.cos(theta)) + uy * math.sin(theta)],
        [uy * ux * (1 - math.cos(theta)) + uz * math.sin(theta), math.cos(theta) + uy * uy * (1 - math.cos(theta)),
         uy * uz * (1 - math.cos(theta)) - ux * math.sin(theta)],
        [uz * ux * (1 - math.cos(theta)) - uy * math.sin(theta),
         uz * uy * (1 - math.cos(theta)) + ux * math.sin(theta), math.cos(theta) + uz * uz * (1 - math.cos(theta))]]
    return rotation_matrix

remaining_rotation = 0
remaining_bend = 0
input_string = []
arm_n = 0
state = False
rotation = 0
bend = 0
total_rotation0 = 0
total_bend1 = 0
total_bend2 = 0
total_bend3 = 0
total_bend4 = 0
total_rotation1 = 0
scat = None

def simData():
    global arms
    global input
    global arm_n
    global rotation
    global bend
    global remaining_rotation
    global remaining_bend
    global clawl
    global clawr
    global input_string
    global state
    global total_rotation0
    global total_bend1
    global total_bend2
    global total_bend3
    global total_bend4
    global total_rotation1
    print('startingsimData')
    print (rotation )
    print (remaining_rotation)
    print (state)

    if state:
        if arm_n == 0:
            if total_rotation0 == 0 and int(input_string[0])==0:
                arm_n = arm_n + 1
            else:
                rotation = int(input_string[0])-total_rotation0
                total_rotation0 = total_rotation0 + rotation
                rotation = math.pi/180*rotation
                remaining_rotation = 0

                state = False
                print (rotation)
        if arm_n == 1:
            if total_bend1 == 0 and int(input_string[1])==0:
                arm_n = arm_n + 1
            else:
                bend = int(input_string[1]) - total_bend1
                total_bend1 = total_bend1 + bend
                bend = math.pi / 180 * bend
                remaining_bend = 0
                state = False
        if arm_n == 2:
            if total_bend2 == 0 and int(input_string[2])==0:
                arm_n = arm_n + 1
            else:
                bend = int(input_string[2]) - total_bend2
                total_bend2 = total_bend2 + bend
                bend = math.pi / 180 * bend
                remaining_bend = 0
                state = False
        if arm_n == 3:
            if total_bend1 == 0 and int(input_string[3])==0:
                arm_n = arm_n + 1
            else:
                bend = int(input_string[3]) - total_bend3
                total_bend3 = total_bend3 + bend
                bend = math.pi / 180 * bend
                remaining_bend = 0
                state = False
        if arm_n == 4:
            if total_rotation0 == 0 and int(input_string[4])==0:
                arm_n = arm_n + 1
            else:
                rotation = int(input_string[4]) - total_rotation1
                total_rotation1 = total_rotation1 + rotation
                rotation = math.pi / 180 * rotation
                remaining_rotation = 0
                state = False
        if arm_n == 5:
            pass
            # bend = math.pi/180*int(input_string[5])
            # remaining_bend = 0
            # state = False


    if arm_n == 5:
        print ("Arm 5 triggered")
        if bend != 0:
            print("CRAW")
            # print(math.fabs(remaining_bend))
            # print(math.fabs(bend))
            if math.fabs(remaining_bend) < math.fabs(bend):
                matrixr = create_rotation_matrix(clawr[0].bend_axis, bend / 100)
                matrixl = create_rotation_matrix(clawr[0].bend_axis, -bend / 100)
                offset = np.array(clawr[0].points[0])
                for i in range(0, len(clawr)):
                    clawr[i].points = (np.dot(np.array(clawr[i].points) - offset,
                                                np.array(matrixr)) + offset).tolist()
                for i in range(0, len(clawl)):

                    clawl[i].points = (np.dot(np.array(clawl[i].points) - offset,
                                                np.array(matrixl)) + offset).tolist()
                remaining_bend = remaining_bend + bend / 100
            else:
                # print("CRAW bend done")
                remaining_bend = 0
                bend = 0

    else:
        print ('else triggered')
        if rotation != 0:
            print("rotate isnt zero!!")
            print(rotation)
            print (remaining_rotation)
            if math.fabs(remaining_rotation) < math.fabs(rotation):
                matrix = create_rotation_matrix(arms[arm_n].rotation_axis(), rotation / 100)
                print("rotating around ", arms[arm_n].rotation_axis())

                if len(arms) - 1 > arm_n:
                    for i in range(arm_n, len(arms)):
                        arms[i].points = (np.dot(np.array(arms[i].points) - np.array(arms[arm_n].points)[0],
                                                np.array(matrix)) + np.array(arms[arm_n].points)[0]).tolist()

                        arms[i].bend_axis = (np.dot(np.array(arms[i].bend_axis),
                                                    np.array(matrix))).tolist()
                        # print("arm", i, " points = ", arms[i].points)
                        # print("arm", i, " bend_axis = ", arms[i].bend_axis)
                remaining_rotation = remaining_rotation + rotation / 100
            else:
                rotation = 0
                remaining_rotation = 0
                state = True
                arm_n = arm_n + 1

        if bend != 0:
            print("bend isnt zero!!")
            # print(math.fabs(remaining_bend))
            # print(math.fabs(bend))
            if math.fabs(remaining_bend) < math.fabs(bend):

                matrix = create_rotation_matrix(arms[arm_n].bend_axis, bend/100)
                temp = np.array(arms[arm_n].points[0])
                if len(arms)-1 > arm_n:
                    for i in range(arm_n+1, len(arms)):
                        arms[i].points = (np.dot(np.array(arms[i].points) - temp,
                                                np.array(matrix)) + temp).tolist()
                        # print("arm ", i, " points", arms[i].points)
                        arms[i].bend_axis = (np.dot(np.array(arms[i].bend_axis - temp),
                                                    np.array(matrix)) + temp).tolist()
                arms[arm_n].points = (np.dot(np.array(arms[arm_n].points) - temp,
                                            np.array(matrix)) + temp).tolist()
                remaining_bend = remaining_bend + bend/100
            else:
                # print("bend done")
                remaining_bend = 0
                bend = 0
                arm_n = arm_n + 1
    yield arms

def simPoints(simData):
    global scat

    x_coordinates = np.array([])
    y_coordinates = np.array([])
    z_coordinates = np.array([])
    for i in range(0, len(simData)):
        # print ("i: " + str(i))
        # print("simData" + str(simData[i].points))

        x_coordinates = np.append(x_coordinates, [simData[i].points[0][0], simData[i].points[1][0]])
        y_coordinates = np.append(y_coordinates, [simData[i].points[0][1], simData[i].points[1][1]])
        z_coordinates = np.append(z_coordinates, [simData[i].points[0][2], simData[i].points[1][2]])

    scat.set_data(x_coordinates.tolist(),y_coordinates.tolist())
    scat.set_3d_properties(z_coordinates.tolist())

    return scat,

class ArmSimulation(HardwareAbstractClass):

    def init(self):
        # print("Overload hardware init function!")
        self.window = None
        # sim = Drawing()

        
        # scat, = plt.plot([], [], [], '-bo', ms=5)
        # scat2, = plt.plot([], [], [], '-bo', ms=10)

        arm0 = Arm([[10, 10, 10], [10, 10, 60]], [1, 0, 0])
        arm1 = Arm([[10, 10, 60], [10, 40, 100]], [1, 0, 0])
        arm2 = Arm([[10, 40, 100], [10, 90, 120]], [1, 0, 0])
        arm3 = Arm([[10, 90, 120], [10, 100, 120]], [1, 0, 0])

        arm4 = Arm([[10,100, 120], [5, 110, 120]], [0, 0, 1])
        arm5 = Arm([[5, 110, 120], [10, 130, 120]], [0, 0, 1])
        arm6 = Arm([[10, 130, 120], [5, 110, 120]], [0, 0, 1])
        arm7 = Arm([[5, 110, 120], [10, 90, 120]], [0, 0, 1])
        #
        arm8 = Arm([[10, 90, 120], [15, 110, 120]], [0, 0, 1])
        arm9 = Arm([[15, 110, 120], [10, 130, 120]], [0, 0, 1])
        arm10 = Arm([[10, 130, 120], [15, 110, 120]], [0, 0, 1])
        arm11 = Arm([[15, 110, 120], [10, 90, 120]], [0, 0, 1])


        clawr = [arm4, arm5, arm6, arm7]
        clawl = [arm8, arm9, arm10, arm11]
        arms = [arm0, arm1, arm2, arm4, arm5, arm6, arm7, arm8, arm9, arm10, arm11] #,arm1,arm2]

    def init_window(self):
        global sim
        sim = Drawing(self.window)

        global scat
        scat = sim.get_fig().add_subplot()
        # scat2 = plt.plot([], [], [], '-bo', ms=10)

    def update(self, action):
        # print ("Overload classifier update function!")
        pass

    def display(self, window):
        if (self.window is None):
            self.window = window
            self.init_window()
        

    def keyboard(self, key):
        pass

    def mouse_click(self, x, y):
        pass