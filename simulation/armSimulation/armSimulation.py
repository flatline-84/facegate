from matplotlib import pyplot as plt
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3
import math
import numpy as np
import time


rotateRightX = False
rotateLeftX = False
rotateUp = False
rotateDown = False

armLower = np.array([[10, 10, 10], [10, 10, 40]])
armMiddle = np.array([[10, 10, 40], [10, 10, 80]])
armUpper = np.array([[10, 10, 80], [10, 10, 120]])

xCoordinates = np.array([])
yCoordinates = np.array([])
zCoordinates = np.array([])

def simData():
    global rotateRightX
    global rotateLeftX
    global rotateDown
    global rotateUp
    global armLower
    global armMiddle
    global armUpper

    yield armLower, armMiddle, armUpper

def simPoints(simData):
    armLower, armMiddle, armUpper = simData[0], simData[1], simData[2]
    xCoordinates = np.array([])
    yCoordinates = np.array([])
    zCoordinates = np.array([])

    for i in armLower, armMiddle, armUpper:
        xCoordinates = np.append(xCoordinates, (i[0][0], i[1][0]))
        yCoordinates = np.append(yCoordinates, (i[0][1], i[1][1]))
        zCoordinates = np.append(zCoordinates, (i[0][2], i[1][2]))

    scat.set_data(xCoordinates, yCoordinates)
    scat.set_3d_properties(zCoordinates)
    return scat,

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(0, 200)
ax.set_ylim(0, 200)
ax.set_zlim(0, 200)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')


ax.set_axis_on()
scat, = plt.plot(xCoordinates, yCoordinates, zCoordinates, '-bo', ms=10)

ani = animation.FuncAnimation(fig, simPoints, simData, blit=True,
                              interval=10, repeat=True)
plt.show()