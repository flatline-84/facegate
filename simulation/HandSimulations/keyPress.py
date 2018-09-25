import curses
import os

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
key = stdscr.getkey()
print(str(key))

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
print(str(key))