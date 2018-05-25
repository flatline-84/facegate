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

    window.register_keyboard(inputDevice.keyboard)
    window.register_keyboard(classifier.keyboard)
    window.register_keyboard(hardware.keyboard)

    window.register_mouse(inputDevice.mouse_click)
    window.register_mouse(classifier.mouse_click)
    window.register_mouse(hardware.mouse_click) 

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

        hardware.update(inputDevice.getData())
        hardware.display(window)

        # hardware.connect()

        window.update()
        window.update_idletasks() 