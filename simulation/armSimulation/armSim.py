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

        self.ax.set_xlim(-200, 200)
        self.ax.set_ylim(-200, 200)
        self.ax.set_zlim(-200, 200)
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


sim = Drawing()
scat, = plt.plot([], [], [], '-bo', ms=10)
scat2, = plt.plot([], [], [], '-bo', ms=10)

arm0 = Arm([[10, 10, 10], [10, 10, 60]], [1, 0, 0])
arm1 = Arm([[10, 10, 60], [10, 60, 60]], [1, 0, 0])
arm2 = Arm([[10, 60, 60], [10, 90, 90]], [1, 0, 0])
arm3 = Arm([[10, 90, 90], [20, 90, 120]], [1, 0, 0])

arms = [arm0, arm1, arm2, arm3]#,arm1,arm2]

arm_n = 0
rotation = 0
bend = 0
def simData():
    global arms
    global input
    global arm_n
    global rotation
    global bend

    if rotation != 0:
        print("rotation isnt zero!!")
        # print(arms[arm_n].points)

        matrix = create_rotation_matrix(arms[arm_n].rotation_axis(), rotation)
        print("rotating around ", arms[arm_n].rotation_axis())

        if len(arms)-1 > arm_n:
            for i in range(arm_n, len(arms)):
                arms[i].points = (np.dot(np.array(arms[i].points)-np.array(arms[arm_n].points)[0],
                                         np.array(matrix))+np.array(arms[arm_n].points)[0]).tolist()

                arms[i].bend_axis = (np.dot(np.array(arms[i].bend_axis),
                                            np.array(matrix))).tolist()
                print("arm", i, " points = ", arms[i].points)
                print("arm", i, " bend_axis = ", arms[i].bend_axis)
    rotation = 0

    if bend != 0:
        print("bend isnt zero!!")
        print("len(arms) = ", len(arms))
        print("arm ", arm_n, " points", arms[arm_n].points)
        matrix = create_rotation_matrix(arms[arm_n].bend_axis, bend)
        temp = np.array(arms[arm_n].points)[0]
        if len(arms)-1 > arm_n:
            for i in range(arm_n+1, len(arms)):
                arms[i].points = (np.dot(np.array(arms[i].points) - temp,
                                         np.array(matrix)) + temp).tolist()
                print("arm ", i, " points", arms[i].points)
                arms[i].bend_axis = (np.dot(np.array(arms[i].bend_axis - temp),
                                            np.array(matrix)) + temp).tolist()
        arms[arm_n].points = (np.dot(np.array(arms[arm_n].points) - temp,
                                     np.array(matrix)) + temp).tolist()

        print("bend done")
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

sim.fig.canvas.mpl_connect('key_press_event', press)
ani = animation.FuncAnimation(sim.fig, simPoints, simData, blit=True, interval=10, repeat=True)

plt.show()

