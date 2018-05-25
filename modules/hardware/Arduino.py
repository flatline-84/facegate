from ..abstract.HardwareAbstract import HardwareAbstractClass
import serial, time

class Servo():

    def __init__(self, servo_id):
        self.servo = servo_id
        self.position = 90

    def checkRotation(self, rot):

        rot = int(rot)
        
        if (rot > 180):
            return 180
        if (rot < 0):
            return 0
        else:
            return rot

    def setRotation(self, rot):
        self.position = self.checkRotation(rot)

    def increaseRotation(self, inc):
        self.position = self.checkRotation(self.position + inc)

    def decreaseRotation(self, dec):
        self.position = self.checkRotation(self.position - dec)

    def getDataPacket(self):
        packet = str(self.servo) + "," + str(self.position)
        # Convert to bytes
        # str.encode(str_)
        return packet

class Arduino(HardwareAbstractClass):

    def init(self):
        # print ("Arduino init!")
        print ("running magical things!")
        # arduino = serial.Serial('/dev/cu.usbmodem1441', 9600, timeout=.1)
        self.arduino  = serial.Serial('/dev/ttyACM0', 19200, timeout=0.1)
        # self.arduino  = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)

        # time.sleep(1)
        # dataVal = b"0"
        # dataVal1 = b"45"
        # dataVal2 = b"90"
        # dataVal3 = b"135"
        # dataVal4 = b"180"

        # self.data = [dataVal,dataVal1,dataVal2,dataVal3,dataVal4]

        self.start = time.time()
        self.counter = 0
        self.elapsed_time = 0

        self.servos = [Servo(1), Servo(2)]
        # pass

    def update(self, action):
        # print ("Doing HW things")

        # print (action)
        if action is not None:
            if (action["Left"]):
                # print ("Action left")
                self.servos[0].increaseRotation(2)
            if (action["Right"]):
                self.servos[0].decreaseRotation(2)

            if (action["Up"]):
                self.servos[1].increaseRotation(2)
            if (action["Down"]):
                self.servos[1].decreaseRotation(2)

        if (self.elapsed_time >= 8):
            print ("Elapsed time: ", self.elapsed_time)
            print("Current time: ", time.time())
            self.connect()
            self.elapsed_time = 0
            self.start = time.time()
        
        self.elapsed_time += time.time() - self.start

    def display(self, window):
        pass

    def keyboard(self, key):
        pass

    def mouse_click(self, x, y):
        pass

    def connect(self):

        # if (self.counter >= len(self.data)):
        #     self.counter = 0

        packet = ""
        for s in self.servos:
            packet += s.getDataPacket()
            packet += ","
        packet = packet[:-1]
        # packet += "Z"

        print ("Packet: ", packet)
        print ("Binary Packet: ", str.encode(packet))

        try:
            self.arduino.write(bytes(str.encode(packet)))
            print('Sent...')
        except:
            print ("Arduino disconnected!")

        # self.arduino.write(bytes(self.data[self.counter]))

        # self.counter += 1
        # data = self.arduino.readline()
        # time.sleep(2)
        # while data == "":
        #     print ("no data recieved ")

        # print("recieved data: " + str(data))
