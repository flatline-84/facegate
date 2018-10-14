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

    # def end(self):
    #     temp = [0, 0, 0]
    #     for i in range(0, len(self.base)):
    #         temp[i] = self.base[i] + self.bendaxis[i] * self.length
    #     return temp


# class armSimulation:
#     def __init__(self):
#
#
#         self.rotateRightX = False
#         self.rotateLeftX = False
#         self.rotateUp = False
#         self.rotateDown = False
#
#                                     # x y z
#         self.armLower = np.array([[10, 10, 10], [10, 10, 40]])
#         self.armMiddle = np.array([[10, 10, 40], [10, 20, 80]])
#         self.armUpper = np.array([[10, 20, 80], [10, 30, 120]])
#
#         self.xCoordinates = np.array([])
#         self.yCoordinates = np.array([])
#         self.zCoordinates = np.array([])
#
#         self.fig = plt.figure()
#         self.ax = self.fig.add_subplot(111, projection='3d')
#
#         self.ax.set_xlim(0, 200)
#         self.ax.set_ylim(0, 200)
#         self.ax.set_zlim(0, 200)
#         self.ax.set_xlabel('X axis')
#         self.ax.set_ylabel('Y axis')
#         self.ax.set_zlabel('Z axis')
#
#         self.ax.set_axis_on()

# sim = armSimulation()
# scat, = plt.plot(sim.xCoordinates, sim.yCoordinates, sim.zCoordinates, '-bo', ms=10)

sim = Drawing()
# scat, = plt.plot(sim.xCoordinates, sim.yCoordinates, sim.zCoordinates, '-bo', ms=10)
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
    #yield sim.armLower, sim.armMiddle, sim.armUpper

    # arm_n = int(input("arm #"))
    # rotation = int(input("rotation degrees"))
    # bend = int(input("bend degrees"))

    if rotation != 0:
        print("rotation isnt zero!!")
        # print(arms[arm_n].points)

        matrix = create_rotation_matrix(arms[arm_n].rotation_axis(), rotation)
        print("rotating around ", arms[arm_n].rotation_axis())
        # arms[arm_n].bend_axis = (np.dot(np.array(arms[arm_n].bend_axis)-np.array(arms[arm_n].points)[0],
        #                              np.array(matrix))+np.array(arms[arm_n].points)[0]).tolist()
        # print(arms[arm_n].points)
        if len(arms)-1 > arm_n:
            for i in range(arm_n, len(arms)):
                arms[i].points = (np.dot(np.array(arms[i].points)-np.array(arms[arm_n].points)[0],
                                         np.array(matrix))+np.array(arms[arm_n].points)[0]).tolist()
                # arms[i].bend_axis = (np.dot(np.array(arms[i].bend_axis-np.array(arms[arm_n].points)[0]),
                #                             np.array(matrix))+np.array(arms[arm_n].points)[0]).tolist()
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

        # matrix = create_rotation_matrix(arms[arm_n].bend_axis, bend)
        # if len(arms) > arm_n:
        #     temp = np.array(arms[arm_n].points)[0] ;
        #     for i in range(arm_n, len(arms)):
        #         arms[i].points = (np.dot(np.array(arms[i].points)-np.array(arms[arm_n].points)[0],
        #                                  np.array(matrix))+np.array(arms[arm_n].points)[0]).tolist()
        #         arms[i].bend_axis = (np.dot(np.array(arms[i].bend_axis-np.array(arms[arm_n].points)[0]),
        #                                     np.array(matrix))+np.array(arms[arm_n].points)[0]).tolist()
        # arms[arm_n].points = (np.dot(np.array(arms[arm_n].points) - np.array(arms[arm_n].points)[0],
        #                              np.array(matrix)) + np.array(arms[arm_n].points)[0]).tolist()
        # bend = 0





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

    # print("x: " + str(x_coordinates))
    # print("axis: " + str(simData[0].rotation_axis()))
    # print ("y: " + str(y_coordinates))
    # print ("z: " + str(z_coordinates))
    scat.set_data(x_coordinates.tolist(),y_coordinates.tolist())
    #scat2.set
    scat.set_3d_properties(z_coordinates.tolist())

    # scat.set_data([simData[0].base[0],
    #                simData[0].end()[0]],
    #               [simData[0].base[1],
    #                simData[0].end()[1]])
    # scat.set_3d_properties([simData[0].base[2],
    #                         simData[0].end()[2]])

    # armLower, armMiddle, armUpper = simData[0], simData[1], simData[2]
    # sim.xCoordinates = np.array([])
    # sim.yCoordinates = np.array([])
    # sim.zCoordinates = np.array([])
    #
    # for i in armLower, armMiddle, armUpper:
    #     sim.xCoordinates = np.append(sim.xCoordinates, (i[0][0], i[1][0]))
    #     sim.yCoordinates = np.append(sim.yCoordinates, (i[0][1], i[1][1]))
    #     sim.zCoordinates = np.append(sim.zCoordinates, (i[0][2], i[1][2]))
    #
    # scat.set_data(sim.xCoordinates, sim.yCoordinates)
    # scat.set_3d_properties(sim.zCoordinates)
    return scat,

# ani = animation.FuncAnimation(sim.fig, simPoints, simData, blit=True, interval=10, repeat=True)

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

