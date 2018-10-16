#Import rendering window 
import tkinter
from WindowManager import WindowManager
# from WindowManagerTwo import WindowManager 


# Import custom modules 
from modules.input import FacialDetection
from modules.classifier import FaceClassifier
from modules.hardware import Arduino
from modules.hardware import FaceSimulation
from modules.hardware import ArmSimulation


if __name__ == '__main__':
    print("Hello world!")
    inputDevice = FacialDetection.FacialDetection()
    classifier = FaceClassifier.FaceClassifier()
    # hardware = Arduino.Arduino()
    hardware = FaceSimulation.FaceSimulation()
    # hardware = ArmSimulation.ArmSimulation()


    inputDevice.init()
    classifier.init()
    hardware.init()

    running = True
    firstRun = True

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
        # is array with landmark points and then original facial image
        data = inputDevice.getData()
        inputDevice.display(window)

        # print ("Data: ", data)

        if (firstRun):
            classifier.set_params(inputDevice.get_dead_zones())
            firstRun = False

        classifier.update(data)
        action = classifier.getAction()
        classifier.display(window)

        # print("Action: ", action)

        # Need to give it facial points to draw, normal actions, NN values
        hardware.update([data[0], action[0], action[1]])
        hardware.display(window)

        # hardware.connect()

        window.update()
        window.update_idletasks() 