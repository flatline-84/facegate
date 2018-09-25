from matplotlib import pyplot as plt
from matplotlib import animation


up = False
right = False
left = False
down = False
rightup = False
rightdown = False

points = [[20, 10], [30, 10], [35, 20],
         [32, 30], [20, 30], [16, 25],
          [20, 10]]
x = 100
y = 100


def simData():
    pass
    # global x
    # global y
    #
    # if up:
    #     y += 1
    #     if right:
    #         x += 1
    #     if left:
    #         x -= 1
    #     yield x, y
    # elif down:
    #     y -= 1
    #     if right:
    #         x += 1
    #     if left:
    #         x -= 1
    #     yield x, y
    # elif right:
    #     x += 1
    #     yield x, y
    # elif left:
    #     x -= 1
    #     yield x, y
    # else:
    #     print("stopped")
    #     yield x, y


def simPoints(simData):
    patch = plt.Polygon(points)
    return patch


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

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

poly = plt.Polygon(points)
# scat, = plt.plot([], [], 'bo', ms=10)
patch = ax.add_patch(poly)
fig.canvas.mpl_connect('key_press_event', press)
fig.canvas.mpl_connect('key_release_event', release)
ani = animation.FuncAnimation(fig, simPoints, simData, blit=False,
                              interval=10, repeat=True)
plt.show()

