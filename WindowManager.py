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
        self.run()

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
        print ("pressed", repr(event.char))

        # return event.char        
        if (event.char == 'q'):
            self.stop()

    def mouse(self, event):
        self.root.focus_set()
        print ("clicked at", event.x, event.y)


    # Main function for tkinter where everything initializes
    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        # Basic configuration for window
        self.root.title("Facegate")
        # self.root.geometry("640x480")
        self.root.geometry("1280x480")
        self.root.configure(background = "white")

        # Add our event handlers
        self.root.bind("<Key>", self.key)
        self.root.bind("<Button-1>", self.mouse)
        
        # Initialize logging window
        Label(self.root, text="Log Output").grid(row=0, column=0, sticky=W)
        self.scrollbar = Scrollbar(self.root)
        self.log_text_frame = Text(self.root)
        self.line_number = 1
        self.scrollbar.grid(row=1, column=0, sticky=W)
        self.log_text_frame.grid(row=1, column=0, sticky=N)
        # Config scrollbar for logging window
        self.scrollbar.config(command=self.log_text_frame.yview)
        self.log_text_frame.config(yscrollcommand=self.scrollbar.set)

        # Organize image
        self.im = Image.open('numbered.jpg')
        # self.im = self.im.resize((int(480*0.66), int(640*0.66)), Image.ANTIALIAS)
        self.tkimg = ImageTk.PhotoImage(self.im)
        # self.tkimg = PhotoImage(file="./numbered.jpg")

        # Label(self.root, text="Image Output").grid(row=0, column=1, sticky=E)
        self.imglabel = Label(self.root, image=self.tkimg).grid(row=0, column=1,rowspan=2,  sticky=E)

        # Configure column weights
        self.root.grid_columnconfigure(0, weight=4)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=4)
        self.root.grid_rowconfigure(2, weight=2)


        # quote = """HAMLET: To be, or not to be--that is the question:
        # Whether 'tis nobler in the mind to suffer
        # The slings and arrows of outrageous fortune
        # Or to take arms against a sea of troubles
        # And by opposing end them. To die, to sleep--
        # No more--and by a sleep to say we end
        # The heartache, and the thousand natural shocks
        # That flesh is heir to. 'Tis a consummation
        # Devoutly to be wished."""
        # self.log_text_frame.insert(END, quote) 


        # self.shutdown_flag = threading.Event()

        # self.root.mainloop()
        self._stop_event = False



    def print(self, text):
        self.log_text_frame.insert(END, str(self.line_number) +": ")
        self.log_text_frame.insert(END, text+"\n") 
        self.log_text_frame.see("end")

        self.line_number += 1
    
    def update(self):
        self.root.update()

    def update_idletasks(self):
        self.root.update_idletasks()