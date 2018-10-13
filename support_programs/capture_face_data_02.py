### This program is used for capturing categorized face data to train the neural network ##

import numpy as np
import cv2
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import sys
import os

import os
from PIL import Image
import operator
from functools import reduce

# Increment this value if your webcam does not work
_WEBCAM = 0
_SIZE = 350

_EQUALIZER = False

# Program running
running = True
# If and what to save
save = None
# Output folder
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out_test")
# Name for saving files
name = None
im = None


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


def save_image(folder_name):
    new_path = os.path.join(out, folder_name)
    # print(new_path)

    if (not os.path.isdir(new_path)):
        os.mkdir(new_path)
        print("Making new folder for %s!" % folder_name)

    i = 0

    # for f in os.listdir(new_path):
    while os.path.exists(os.path.join(new_path, "m-" + name + "-" + "%i.png" % i)):
        i += 1

    filename = "m-" + name + "-" + str(i) + ".png"

    new_file = os.path.join(new_path, filename)
    print(new_file)
    # ret = cv2.imwrite(new_file, im)

    # with open(new_file, 'w') as f:
    # result.save(f)
    im.save(new_file)
    # print("Image saved to disk")


# Button callback functions
def AngerCallback():
    save_image("anger")


def NeutralCallback():
    save_image("neutral")


def ScreamCallback():
    save_image("scream")


def SmileCallback():
    save_image("smile")


def QuitCallback():
    global running
    running = False


def EqualCallback():
    global _EQUALIZER
    _EQUALIZER = not _EQUALIZER


def equalize(h):
    lut = []

    for b in range(0, len(h), 256):

        # step size
        step = reduce(operator.add, h[b:b + 256]) / 255

        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + h[i + b]

    return lut


if __name__ == '__main__':

    # Get user's name before running the program
    if (len(sys.argv) != 2):
        print("Please only add your name as a command line argument")
        print("EG: python3 capture_face_data.py peter")
        print("And make sure you're running this from the support_programs folder! Otherwise it'll misbehave :)")
        print("Your pictures will be stored in a folder called 'out'")
        exit(1)

    # global name
    name = sys.argv[1]

    if (not os.path.isdir(out)):
        os.mkdir(out)
        print("Making new folder for %s!" % out)

    ## Setup Tkinter
    # Tkinter drawing code
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", callback)

    ## Basic configuration for window
    root.title("DCNN Face Maker")
    # root.geometry("640x480")
    root.geometry("768x616")
    # root.geometry("1280x480")
    # self.root.geometry("1920x480")

    root.configure(background="white")

    ## Add our event handlers
    root.bind("<Key>", key)
    root.bind("<Button-1>", mouse)

    # global im
    im = Image.open('../numbered.jpg')
    tkimg = ImageTk.PhotoImage(im)
    # self.tkimg = PhotoImage(file="./numbered.jpg")
    imglabel = Label(root, image=tkimg)
    imglabel.grid(row=0, column=0, columnspan=6, sticky=N)

    ## Setup the buttons
    button_Anger = tk.Button(root, text='Anger', command=AngerCallback)
    button_Anger.grid(row=1, column=0)

    button_Neutral = tk.Button(root, text='Neutral', command=NeutralCallback)
    button_Neutral.grid(row=1, column=1)

    button_Scream = tk.Button(root, text='Scream', command=ScreamCallback)
    button_Scream.grid(row=1, column=2)

    button_Smile = tk.Button(root, text='Smile', command=SmileCallback)
    button_Smile.grid(row=1, column=3)

    button_Quit = tk.Button(root, text='Quit', command=QuitCallback)
    button_Quit.grid(row=1, column=4)

    button_Equal = tk.Button(root, text='EQUAL', command=EqualCallback)
    button_Equal.grid(row=1, column=5)

    # Initialize webcam
    cap = cv2.VideoCapture(_WEBCAM)

    # Initialize Face Cascade
    try:
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        print("Loaded the face cascade")
    except:
        print(
            "Can't find face cascade file. Please make sure there is a file called 'haarcascade_frontalface_default.xml' in this directory")
        exit(1)

    print("Press 'q' to quit the program...")

    if (cap.isOpened() == False):
        print("Cannot open webcam. Please check your _WEBCAM variable")
        exit(1)

    while (running):
        ret, frame = cap.read()

        if ret == True:
            frame = cv2.flip(frame, 1)
            # cv2.imshow('image', frame)
            # frame = cv2.resize(frame, (768, 576))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # im = frame

            faces = faceCascade.detectMultiScale(frame,
                                                 scaleFactor=1.2,
                                                 minNeighbors=8,
                                                 minSize=(50, 50),
                                                 flags=cv2.CASCADE_SCALE_IMAGE
                                                 )

            # # Draw the rectangle
            # for (x, y, w, h) in faces:
            #     # mid_point_x = x + (w/2)
            #     # mid_point_y = y + (h/2)
            #     # scale_factor = (_SIZE / w)
            #     # w = int(w * scale_factor)
            #     # h = int(h * scale_factor)

            #     # x = int(mid_point_x - (w / 2))
            #     # y = int(mid_point_y - (h / 2))

            #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #     # print ("Size: ", w, h)

            # Needed to save the file
            # im = frame

            for (x, y, w, h) in faces:
                # Get original size of face
                # im = np.array(image)
                # print(im)
                im = frame[y:(y + h), x:(x + w)]

                # mid_point_x = x + (w/2)
                # mid_point_y = y + (h/2)

                # scale_factor = (_SIZE / w)

                im = Image.fromarray(im).resize((_SIZE, _SIZE))

                # w = int(w * scale_factor)
                # h = int(h * scale_factor)

                # x = int(mid_point_x - (w / 2))
                # y = int(mid_point_y - (h / 2))
                # y, x
                # Resize face here

            # frame = frame[...,::-1]
            # image = Image.fromarray(frame)
            image = im

            if (_EQUALIZER):
                # calculate lookup table
                lut = equalize(image.histogram())
                # map image through lookup table
                image = image.point(lut)

            # im = image
            tkimg = ImageTk.PhotoImage(image)
            # tkimg = ImageTk.PhotoImage(im)

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