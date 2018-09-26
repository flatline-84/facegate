from matplotlib import pyplot as plt
from matplotlib import animation



up = False
right = False
left = False
down = False
rightup = False
rightdown = False


squarex = [2, 2, 4, 4, 2]
squarey = [2, 4, 4, 2, 2]


def simData():
    global squarex
    global squarey

    if up:
        squarey = [x + 1 for x in squarey]
        if right:
            squarex = [x + 1 for x in squarex]
        if left:
            squarex = [x - 1 for x in squarex]
        yield squarex, squarey

    elif down:
        squarey = [x - 1 for x in squarey]

        if right:
            squarex = [x + 1 for x in squarex]

        if left:
            squarex = [x - 1 for x in squarex]

        yield squarex, squarey
    elif right:
        squarex = [x + 1 for x in squarex]

        yield squarex, squarey
    elif left:
        squarex = [x - 1 for x in squarex]
        yield squarex, squarey
    else:
        yield squarex, squarey

def simPoints(simData):
    squarex, squarey = simData[0], simData[1]
    scat.set_data(squarex, squarey)
    print (squarex)
    print (squarey)
    return scat,



def press(event):
    if event.key == 'up':
        global up
        up = True
    if event.key == 'down':
        global down
        down = True
    if event.key == 'right':
        global right
        right = True
    if event.key == 'left':
        global left
        left = True


def release(event):
    if event.key == 'up':
        global up
        up = False
    if event.key == 'down':
        global down
        down = False
    if event.key == 'right':
        global right
        right = False
    if event.key == 'left':
        global left
        left = False



fig = plt.figure()
ax = fig.add_subplot(111)

ax.set_xlim(0, 25)
ax.set_ylim(0, 25)

scat, = plt.plot(squarex, squarey, '-bo', ms=10)

fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('key_release_event', release)
ani = animation.FuncAnimation(fig, simPoints, simData, blit=False,
                              interval=10, repeat=True)
plt.show()


