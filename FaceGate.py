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

    while(running):
        inputDevice.update()
        data = inputDevice.getData()

        print ("Data: ", data)

        classifier.update(data)
        action = classifier.getAction()

        print("Action: ", action)

        hardware.update(action)


        # Remove this to have the program run indefinitely
        running = False