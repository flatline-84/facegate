from matplotlib import pyplot as plt
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3
import math
import numpy as np
import time


class armSimulation:
    def __init__(self):

        self.armLower = np.array([[10, 10, 10], [10, 10, 40]])
        self.armMiddle = np.array([[10, 10, 40], [10, 10, 80]])
        self.armUpper = np.array([[10, 10, 80], [10, 10, 120]])

        self.xCoordinates = np.array([])
        self.yCoordinates = np.array([])
        self.zCoordinates = np.array([])

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(0, 200)
        self.ax.set_ylim(0, 200)
        self.ax.set_zlim(0, 200)
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        self.ax.set_axis_on()



sim = armSimulation()
scat, = plt.plot(sim.xCoordinates, sim.yCoordinates, sim.zCoordinates, '-bo', ms=10)


def simData():
    yield sim.armLower, sim.armMiddle, sim.armUpper

def simPoints(simData):
    global scat
    armLower, armMiddle, armUpper = simData[0], simData[1], simData[2]
    sim.xCoordinates = np.array([])
    sim.yCoordinates = np.array([])
    sim.zCoordinates = np.array([])

    for i in armLower, armMiddle, armUpper:
        sim.xCoordinates = np.append(sim.xCoordinates, (i[0][0], i[1][0]))
        sim.yCoordinates = np.append(sim.yCoordinates, (i[0][1], i[1][1]))
        sim.zCoordinates = np.append(sim.zCoordinates, (i[0][2], i[1][2]))

    scat.set_data(sim.xCoordinates, sim.yCoordinates)
    scat.set_3d_properties(sim.zCoordinates)
    return scat,



ani = animation.FuncAnimation(sim.fig, simPoints, simData, blit=True,
                              interval=10, repeat=True)
plt.show()


