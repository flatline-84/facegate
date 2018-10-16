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

paused = False

def keyboard_event(key):
    global paused
    if key == ' ':
        paused = not paused

if __name__ == '__main__':
    print("Initiating program procedures...")
    inputDevice =       FacialDetection.FacialDetection()
    classifier =        FaceClassifier.FaceClassifier()
    hardwareArduino =   Arduino.Arduino()
    hardware =          FaceSimulation.FaceSimulation()
    hardwareSim =       ArmSimulation.ArmSimulation()


    inputDevice.init()
    classifier.init()
    hardware.init()
    hardwareArduino.init()
    hardwareSim.init()

    running = True
    firstRun = True

    window = WindowManager()  

    window.register_keyboard(inputDevice.keyboard)
    window.register_keyboard(classifier.keyboard)
    window.register_keyboard(hardware.keyboard)
    window.register_keyboard(hardwareArduino.keyboard)
    window.register_keyboard(hardwareSim.keyboard)
    window.register_keyboard(keyboard_event)

    window.register_mouse(inputDevice.mouse_click)
    window.register_mouse(classifier.mouse_click)
    window.register_mouse(hardware.mouse_click) 
    window.register_mouse(hardwareArduino.mouse_click)
    window.register_mouse(hardwareSim.mouse_click)

    while(running):
        # If user presses 'q' key, program will quit
        if (window.stopped()):
            print ("Killing program")
            window.callback()
            break

        # continue
        if (not paused):
            inputDevice.update()
        # is array with landmark points and then original facial image
        data = inputDevice.getData()
        inputDevice.display(window)

        # print ("Data: ", data)

        if (firstRun):
            classifier.set_params(inputDevice.get_dead_zones())
            firstRun = False

        if (not paused):
            classifier.update(data)
        action = classifier.getAction()
        classifier.display(window)

        # print("Action: ", action)

        if (not paused):
            # Need to give it facial points to draw, normal actions, NN values
            hardware.update([data[0], action[0], action[1]])
            hardwareArduino.update(action)
            hardwareSim.update(hardwareArduino.get_packet_string())
        
        hardware.display(window)
        hardwareArduino.display(window)
        hardwareSim.display(window)

        # hardware.connect()

        window.update()
        window.update_idletasks() 