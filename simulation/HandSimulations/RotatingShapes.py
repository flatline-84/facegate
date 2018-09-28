from matplotlib import pyplot as plt
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3


forward = False
right = False
left = False
backward = False
rightforward = False
rightbackward = False
up = False
down = False

squarex = [2, 2, 4, 4, 2]
squarey = [2, 4, 4, 2, 2]
squarez = [0, 0, 0, 0, 0]


def simData():
    global squarex
    global squarey
    global squarez

    if forward:
        squarey = [x + 1 for x in squarey]
        if right:
            squarex = [x + 1 for x in squarex]
        if left:
            squarex = [x - 1 for x in squarex]
        yield squarex, squarey, squarez

    elif backward:
        squarey = [x - 1 for x in squarey]

        if right:
            squarex = [x + 1 for x in squarex]

        if left:
            squarex = [x - 1 for x in squarex]

        yield squarex, squarey, squarez
    elif right:
        squarex = [x + 1 for x in squarex]

        yield squarex, squarey, squarez
    elif left:
        squarex = [x - 1 for x in squarex]
        yield squarex, squarey, squarez
    elif up:
        print ("UP")
        squarez = [x + 1 for x in squarez]
        yield squarex, squarey, squarez
    elif down:
        print ("DOWN")
        squarez = [x - 1 for x in squarez]
        yield squarex, squarey,squarez
    else:
        yield squarex, squarey, squarez

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



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim(0, 25)
ax.set_ylim(0, 25)
ax.set_zlim(0, 25)

scat, = plt.plot(squarex, squarey, squarez, '-bo', ms=10)

fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('key_release_event', release)
ani = animation.FuncAnimation(fig, simPoints, simData, blit=False,
                              interval=10, repeat=True)
plt.show()


