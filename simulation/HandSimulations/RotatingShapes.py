from matplotlib import pyplot as plt
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3
import math
import numpy as np
import time


forward = False
right = False
left = False
backward = False
rightforward = False
rightbackward = False
up = False
down = False
rotaterightx = False
rotateleftx = False
rotateup = False
rotatedown =False

squarex = np.array([2, 2, 40, 40, 2])
squarey = np.array([2, 40, 40, 2, 2])
squarez = np.array([0, 0, 0, 0, 0])
squarexyz = np.array([squarex, squarey, squarez])
centerxyz = np.array([[21], [2], [0]])


theta = 0
z_axis_rotation_angle = 0
# rotational_array_x = [[1, 0, 0],
#                       [0, math.cos(theta), -math.sin(theta)],
#                       [0, math.sin(theta), math.cos(theta)]]
#
# rotational_array_z = [[math.cos(theta), -math.sin(theta), 0],
#                       [math.sin(theta), math.cos(theta), 0],
#                       [0, 0, 1]]

ux = 0
uy = 0
uz = 1

uxlr = 1
uylr = 0
uzlr = 0

rotation_axis = [ux, uy, uz] # sets x as default initial axis

direction = math.pi/2

def create_rotation_matrix(ux, uy, uz, theta):
    rotation_matrix = [[math.cos(theta)+ux*ux*(1-math.cos(theta)), ux*uy*(1-math.cos(theta))-uz*math.sin(theta), ux*uz*(1-math.cos(theta))+uy*math.sin(theta)],
                       [uy*ux*(1-math.cos(theta))+uz*math.sin(theta), math.cos(theta)+uy*uy*(1-math.cos(theta)), uy*uz*(1-math.cos(theta))-ux*math.sin(theta)],
                       [uz*ux*(1-math.cos(theta))-uy*math.sin(theta), uz*uy*(1-math.cos(theta))+ux*math.sin(theta), math.cos(theta) + uz*uz*(1-math.cos(theta))]]
    return rotation_matrix

def simData():
    global squarexyz
    global centerxyz
    global theta
    global rotateleftx
    global rotational_array_x
    global rotational_array_z
    global z_axis_rotation_angle
    global direction
    global uxlr
    global uylr
    global uzlr

    if forward:
        squarexyz[1] = [x + 1 for x in squarexyz[1]]
        centerxyz[1] = centerxyz[1] + 1
        if right:
            squarexyz[0] = [x + 1 for x in squarexyz[0]]
            centerxyz[0] = centerxyz[0] + 1
        if left:
            squarexyz[0] = [x - 1 for x in squarexyz[0]]
            centerxyz[0] = centerxyz[0] - 1
        yield squarexyz

    elif backward:
        squarexyz[1] = [x - 1 for x in squarexyz[1]]
        centerxyz[1] = centerxyz[1] - 1

        if right:
            squarexyz[0] = [x + 1 for x in squarexyz[0]]
            centerxyz[0] = centerxyz[0] + 1

        if left:
            squarexyz[0] = [x - 1 for x in squarexyz[0]]
            centerxyz[0] = centerxyz[0] - 1

        yield squarexyz
    elif right:
        squarexyz[0] = [x + 1 for x in squarexyz[0]]
        centerxyz[0] = centerxyz[0] + 1

        yield squarexyz
    elif left:
        squarexyz[0] = [x - 1 for x in squarexyz[0]]
        centerxyz[0] = centerxyz[0] - 1
        yield squarexyz
    elif up:
        print ("UP")
        squarexyz[2] = [x + 1 for x in squarexyz[2]]
        centerxyz[2] = centerxyz[2] + 1
        yield squarexyz

    elif down:
        print ("DOWN")
        squarexyz[2] = [x - 1 for x in squarexyz[2]]
        centerxyz[2] = centerxyz[2] - 1
        yield squarexyz

    elif rotaterightx:
        theta = math.pi / 100
        direction = direction - theta
        ux = 0
        uy = 0
        uz = 1

        rotation_axis = [ux, uy, uz]  # sets x as default initial axis
        rotation_matrix = create_rotation_matrix(ux,uy,uz, theta)

        squarexyz = np.subtract(squarexyz, centerxyz)
        squarexyz = np.dot(rotation_matrix, squarexyz)
        squarexyz = np.add(squarexyz, centerxyz)

        yield squarexyz


    elif rotateleftx:

        theta = -math.pi / 100
        direction = direction - theta
        ux = 0
        uy = 0
        uz = 1
        rotation_axis = [ux, uy, uz]  # sets x as default initial axis

        rotation_matrix = create_rotation_matrix(ux,uy,uz, theta)

        squarexyz = np.subtract(squarexyz, centerxyz)
        squarexyz = np.dot(rotation_matrix, squarexyz)
        squarexyz = np.add(squarexyz, centerxyz)

        yield squarexyz

    elif rotateup:
        theta = math.pi / 100

        uxlr = math.sin(direction)
        uylr = math.cos(direction)
        uzlr = 0

        rotation_matrix = create_rotation_matrix(uxlr,uylr,uzlr, theta)


        squarexyz = np.subtract(squarexyz, centerxyz)
        squarexyz = np.dot(rotation_matrix, squarexyz)
        squarexyz = np.add(squarexyz, centerxyz)
        yield squarexyz

    elif rotatedown:
        theta = -math.pi / 100

        uxlr = math.sin(direction)
        uylr = math.cos(direction)
        uzlr = 0

        rotation_matrix = create_rotation_matrix(uxlr, uylr, uzlr, theta)

        squarexyz = np.subtract(squarexyz, centerxyz)
        squarexyz = np.dot(rotation_matrix, squarexyz)
        squarexyz = np.add(squarexyz, centerxyz)

        yield squarexyz


    else:
        yield squarexyz

def simPoints(simData):
    squarex, squarey, squarez = simData[0], simData[1], simData[2]
    scat.set_data(squarex, squarey)
    scat.set_3d_properties(squarez)
    # print (squarex)
    # print (squarey)
    # print (squarez)
    return scat,



def press(event):
    if event.key == 'up':
        global forward
        forward = True
    if event.key == 'down':
        global backward
        backward = True
    if event.key == 'right':
        global right
        right = True
    if event.key == 'left':
        global left
        left = True
    if event.key == 'z':
        global up
        up = True
    if event.key == 'x':
        global down
        down = True
    if event.key == 'u':
        global rotaterightx
        rotaterightx = True


    if event.key == 'i':
        global rotateleftx
        rotateleftx = True
    if event.key == 'h':
        global rotateup
        rotateup = True
    if event.key == 'j':
        global rotatedown
        rotatedown = True

def release(event):
    if event.key == 'up':
        global forward
        forward = False
    if event.key == 'down':
        global backward
        backward = False
    if event.key == 'right':
        global right
        right = False
    if event.key == 'left':
        global left
        left = False
    if event.key == 'z':
        global up
        up = False
    if event.key == 'x':
        global down
        down = False
    if event.key == 'u':
        global rotaterightx
        rotaterightx = False
    if event.key == 'i':
        global rotateleftx
        rotateleftx = False
    if event.key == 'h':
        global rotateup
        rotateup = False
    if event.key == 'j':
        global rotatedown
        rotatedown = False


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_zlim(0, 100)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

ax.set_axis_on()
scat, = plt.plot(squarex, squarey, squarez, '-bo', ms=10)

fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('key_release_event', release)
ani = animation.FuncAnimation(fig, simPoints, simData, blit=True,
                              interval=10, repeat=True)
plt.show()


