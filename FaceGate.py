#Import rendering window 
import tkinter
from WindowManager import WindowManager 

# Import custom modules 
from modules.input import FacialDetection
from modules.classifier import FaceClassifier
from modules.hardware import Arduino


if __name__ == '__main__':
    print("Hello world!")
    inputDevice = FacialDetection.FacialDetection()
    classifier = FaceClassifier.FaceClassifier()
    hardware = Arduino.Arduino()

    inputDevice.init()
    classifier.init()
    hardware.init()

    running = True

    window = WindowManager()  

    while(running):
        # If user presses 'q' key, program will quit
        if (window.stopped()):
            print ("Killing program")
            window.callback()
            break
  
        # continue
        inputDevice.update()
        data = inputDevice.getData()
        inputDevice.display(window)

        # print ("Data: ", data)

        classifier.update(data)
        action = classifier.getAction()
        classifier.display(window)

        # print("Action: ", action)

        hardware.update(action)
        hardware.display(window)

        window.update()
        window.update_idletasks() 