### This program is used for capturing categorized face data to train the neural network ##

import numpy as np 
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import sys
import os

# Increment this value if your webcam does not work
_WEBCAM = 0

# Program running
running = True
# If and what to save
save = None
# Output folder
out = "out"
# Name for saving files
name = None

# Tkinter functions
def callback():
    root.quit()
    sys.exit(0)

def key(event):
    if (event.char == 'q'):
        global running
        running = False

def mouse(event):
    pass

# Button callback functions
def AngerCallback():
    new_path = os.path.join(out, "anger")

    for f in os.listdir(new_path):
        '''you are here peter'''
        pass
    pass

def NeutralCallback():
    pass

def ScreamCallback():
    pass

def SmileCallback():
    pass

def QuitCallback():
    global running
    running = False

if __name__ == '__main__':

    # Get user's name before running the program
    if (len(sys.argv) != 2):
        print("Please only add your name as a command line argument")
        exit(1)
    
    global name
    name = sys.argv[1]

    ## Setup Tkinter
    # Tkinter drawing code
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", callback)

    ## Basic configuration for window
    root.title("DCNN Face Maker")
    # root.geometry("640x480")
    root.geometry("640x520")
    # root.geometry("1280x480")
    # self.root.geometry("1920x480")

    root.configure(background = "white")

    ## Add our event handlers
    root.bind("<Key>", key)
    root.bind("<Button-1>", mouse)
    
    im = Image.open('../numbered.jpg')
    tkimg = ImageTk.PhotoImage(im)
    # self.tkimg = PhotoImage(file="./numbered.jpg")
    imglabel = Label(root, image=tkimg)
    imglabel.grid(row=0, column=0, columnspan=5, sticky=N)

    ## Setup the buttons
    button_Anger = tk.Button(root, text='Anger', command = AngerCallback)
    button_Anger.grid(row=1, column=0)

    button_Neutral = tk.Button(root, text='Neutral', command = NeutralCallback)
    button_Neutral.grid(row=1, column=1)

    button_Scream = tk.Button(root, text='Scream', command = ScreamCallback)
    button_Scream.grid(row=1, column=2)

    button_Smile = tk.Button(root, text='Smile', command = SmileCallback)
    button_Smile.grid(row=1, column=3)

    button_Quit = tk.Button(root, text='Quit', command = QuitCallback)
    button_Quit.grid(row=1, column=4)

    # Initialize webcam 
    cap = cv2.VideoCapture(_WEBCAM)

    print("Press 'q' to quit the program...")

    if (cap.isOpened() == False):
        print("Cannot open webcam. Please check your _WEBCAM variable")
        exit(1)

    while(running):
        ret, frame = cap.read()

        if ret == True:
            frame = cv2.flip(frame, 1)
            # cv2.imshow('image', frame)

            frame = frame[...,::-1]
            image = Image.fromarray(frame)

            tkimg = ImageTk.PhotoImage(image)
            imglabel.configure(image=tkimg)
            imglabel.image = tkimg

        else:
            running = False

        root.update()
        root.update_idletasks()

    print("Shutting down...")

    cap.release()
    # cv2.destroyAllWindows()

    print("Completed. Thank you for doing the needful.")