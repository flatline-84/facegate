import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import threading
import sys

# class WindowManager(threading.Thread):
class WindowManager():


    # Tkinter specific code
    def __init__(self):
        # threading.Thread.__init__(self)
        # self._stop_event = threading.Event()
        # self.start()
        self.init()

    def stop(self):
        # self._stop_event.set()
        self._stop_event = True

    def stopped(self):
        # return self._stop_event.is_set()
        return self._stop_event

    def callback(self):
        self.root.quit()
        # self.shutdown_flag.set()
        # self.join()
        sys.exit(0)


    # Event handlers
    def key(self, event):
        # print ("pressed", repr(event.char))
        print_str = "Key Pressed: " + repr(event.char)
        self.print(print_str)

        # return event.char        
        if (event.char == 'q'):
            self.stop()

    def mouse(self, event):
        self.root.focus_set()
        print_str = "Click at: " + str(event.x) + ":" + str(event.y)
        
        self.print(print_str)



    # Main function for tkinter where everything initializes
    def init(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        ## Basic configuration for window
        self.root.title("Facegate")
        # self.root.geometry("640x480")
        self.root.geometry("1280x480")
        self.root.configure(background = "white")

        ## Add our event handlers
        self.root.bind("<Key>", self.key)
        self.root.bind("<Button-1>", self.mouse)
        
        ## Initialize logging window
        # Label(self.root, text="Log Output").grid(row=0, column=0, sticky=W)
        self.scrollbar = Scrollbar(self.root)
        self.log_text_frame = Text(self.root)
        self.line_number = 1
        # self.scrollbar.grid(row=0, column=0, sticky=W)
        self.log_text_frame.grid(row=0, column=0, sticky=N)
        
        ## Config scrollbar for logging window
        self.scrollbar.config(command=self.log_text_frame.yview)
        self.log_text_frame.config(yscrollcommand=self.scrollbar.set)

        ## Information Window
        self.info_text_frame = Text(self.root)
        self.info_text_frame.grid(row=1, column=0)
        self.info_text = "\
        Welcome to Facegate!\n\
        Peter Kydas - s3485580\n\
        Daniel Sosa Haby - s3486824\n\
        Marcela Klocker - s3487194"

        self.info_text_frame.insert(END, self.info_text)

        ## Organize image 
        self.im = Image.open('numbered.jpg')
        # self.im = self.im.resize((int(480*0.66), int(640*0.66)), Image.ANTIALIAS)
        self.tkimg = ImageTk.PhotoImage(self.im)
        # self.tkimg = PhotoImage(file="./numbered.jpg")
        self.imglabel = Label(self.root, image=self.tkimg)
        self.imglabel.grid(row=0, column=1,rowspan=3,  sticky=E)

        ## Configure column weights
        self.root.grid_columnconfigure(0, weight=4)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=7)
        # self.root.grid_rowconfigure(2, weight=25)

        self._stop_event = False



    def print(self, text):
        self.log_text_frame.insert(END, str(self.line_number) +": ")
        self.log_text_frame.insert(END, text+"\n") 
        self.log_text_frame.see("end")

        self.line_number += 1
    
    def update_image(self, img):
        # im = Image.open(img)
        # self.tkimg = ImageTk.PhotoImage(img)
        # print (type(self.imglabel))
        tkimg = ImageTk.PhotoImage(img)
        self.imglabel.configure(image=tkimg)
        self.imglabel.image = tkimg

    def update(self):
        self.root.update()

    def update_idletasks(self):
        self.root.update_idletasks()