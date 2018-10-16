import curses
import os
from matplotlib import pyplot as plt
from matplotlib import animation
import mpl_toolkits.mplot3d.axes3d as p3

#
# stdscr = curses.initscr()
# curses.noecho()
# curses.cbreak()
# stdscr.keypad(True)
# key = stdscr.getkey()
# print(str(key))
#
# curses.nocbreak()
# stdscr.keypad(False)
# curses.echo()
# curses.endwin()
# print(str(key))


def on_key(event):
    print('you pressed', event.key, event.xdata, event.ydata)
fig = plt.figure()
ax = fig.add_subplot(111)
cid = fig.canvas.mpl_connect('key_press_event', on_key)
plt.show()