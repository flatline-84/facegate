from ..abstract.HardwareAbstract import HardwareAbstractClass
import serial, time


class Arduino(HardwareAbstractClass):

    def init(self):
        # print ("Arduino init!")
        pass

    def update(self, action):
        # print ("Doing HW things")
        pass

    def display(self, window):
        pass

    def keyboard(self, key):
        pass

    def mouse_click(self, x, y):
        pass



    def connect(self):
        print ("running magical things!")
        arduino = serial.Serial('/dev/cu.usbmodem1441', 9600, timeout=.1)
        time.sleep(1)
        dataVal = b"0"
        dataVal1 = b"45"
        dataVal2 = b"90"
        dataVal3 = b"135"
        dataVal4 = b"180"

        list = [dataVal,dataVal1,dataVal2,dataVal3,dataVal4]

        while True:
            for i in list:
                arduino.write(bytes(i))
                print('Sent...')
                data = arduino.readline()
                time.sleep(.5)
                while data == "":
                    print ("no data recieved ")

                print("recieved data: " + str(data))
