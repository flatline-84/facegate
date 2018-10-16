from matplotlib import pyplot as plt
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3
import math
import numpy as np
import time


class Drawing:
    def __init__(self):

        self.fig = plt.figure()
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


class Arm:
    def __init__(self, points, bend_axis):

        self.points = points
        self.bend_axis = bend_axis

    def rotation_axis(self):
        x = self.points[1][0] - self.points[0][0]
        y = self.points[1][1] - self.points[0][1]
        z = self.points[1][2] - self.points[0][2]
        mag = math.sqrt(x*x+y*y+z*z)
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


def rotation_axis(u):
    x = u[0]
    y = u[1]
    z = u[2]
    mag = math.sqrt(x*x+y*y+z*z)
    return [x/mag, y/mag, z/mag]

remaining_rotation = 0
remaining_bend = 0

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

    if rotation != 0:
        if math.fabs(remaining_rotation) < math.fabs(rotation):
            matrix = create_rotation_matrix(arms[arm_n].rotation_axis(), rotation/100)
            # print("rotating around ", arms[arm_n].rotation_axis())

            if len(arms)-1 > arm_n:
                for i in range(arm_n, len(arms)):
                    arms[i].points = (np.dot(np.array(arms[i].points)-np.array(arms[arm_n].points)[0],
                                             np.array(matrix))+np.array(arms[arm_n].points)[0]).tolist()

                    arms[i].bend_axis = (np.dot(np.array(arms[i].bend_axis),
                                                np.array(matrix))).tolist()
                    # print("arm", i, " points = ", arms[i].points)
                    # print("arm", i, " bend_axis = ", arms[i].bend_axis)
            remaining_rotation = remaining_rotation + rotation/100
        else:
            rotation = 0
            remaining_rotation = 0

    if bend != 0:
        print("bend isnt zero!!")
        print(math.fabs(remaining_bend))
        print(math.fabs(bend))
        if math.fabs(remaining_bend) < math.fabs(bend):

            matrix = create_rotation_matrix(arms[arm_n].bend_axis, bend/100)
            temp = np.array(arms[arm_n].points)[0]
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

def press(event):
    global arm_n
    global rotation
    global bend
    if event.key == "up":
        arm_n = int(input("arm #"))
        rotation = math.pi/180*int(input("rotation degrees"))
        bend = math.pi/180*int(input("bend degrees"))



sim = Drawing()
scat, = plt.plot([], [], [], '-bo', ms=5)
scat2, = plt.plot([], [], [], '-bo', ms=10)

arm0 = Arm([[10, 10, 10], [10, 10, 60]], [1, 0, 0])
arm1 = Arm([[10, 10, 60], [10, 40, 100]], [1, 0, 0])
arm2 = Arm([[10, 40, 100], [10, 90, 120]], [1, 0, 0])
arm3 = Arm([[10, 90, 120], [10, 100, 120]], [1, 0, 0])

arm4 = Arm([[10, 90, 120],[5, 110, 120]],[1, 0, 0])
arm5 = Arm([[5, 110, 120],[10, 130, 120]],[1, 0, 0])
arm6 = Arm([[10,130, 120],[5, 110, 120]],[1, 0, 0])
arm7 = Arm([[5,110,120],[10, 90, 120]],[1, 0, 0])
#
arm8 = Arm([[10, 90, 120], [15, 110, 120]], [1, 0, 0])
arm9 = Arm([[15, 110, 120], [10, 130, 120]], [1, 0, 0])
arm10 = Arm([[10, 130, 120], [15, 110, 120]], [1, 0, 0])
arm11 = Arm([[15, 110, 120], [10, 90, 120]], [1, 0, 0])


clawr = [arm4, arm5, arm6, arm7]
clawl = [arm8, arm9, arm10, arm11]
arms = [arm0, arm1, arm2, arm4, arm5, arm6, arm7, arm8, arm9, arm10, arm11] #,arm1,arm2]

arm_n = 0
rotation = 0
bend = 0


sim.fig.canvas.mpl_connect('key_press_event', press)
ani = animation.FuncAnimation(sim.fig, simPoints, simData, blit=True, interval=10, repeat=True)

plt.show()

