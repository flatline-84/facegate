from ..abstract.HardwareAbstract import HardwareAbstractClass
import serial, time
import operator

# For NN to trigger
_THRESHOLD = 0.80

# b90s90e90w90h90f90

class Joint:                 #char to be used in packet 
    def __init__(self, nome, uniq_char, rot):
        self.name = nome
        self.rotation = rot
        self.uniq_char = uniq_char
    def set_rotation(self, rot):
        if (rot > 180):
            rot = 180
        if (rot < 0):
            rot = 0
        self.rotation = rot

    def increase_rotation(self, value):
        self.set_rotation(self.rotation + value)
    def decrease_rotation(self, value):
        self.increase_rotation(-value)
    
    def get_string(self):
        return [str.encode(self.uniq_char), bytes([self.rotation])]

class Arm:
    def __init__(self):

        self.defaults = [90, 55, 75, 45, 90, 60]
        self.arm = {
            "base":     Joint("base", 'b', 90),
            "shoulder": Joint("shoulder", 's', 90),
            "elbow":    Joint("elbow", 'e', 90),
            "wrist":    Joint("wrist", 'w', 90),
            "hand":     Joint("hand", 'h', 90),
            "fingers":  Joint("fingers", 'f', 90)
        }
        self.reset_arm()

    def reset_arm(self):
        i = 0
        for k, j in self.arm.items():
            j.set_rotation(self.defaults[i])
            i+=1

    def left(self, rot):
        self.arm["base"].decrease_rotation(rot)
        self.arm["hand"].decrease_rotation(rot)
    
    def right(self, rot):
        self.arm["base"].increase_rotation(rot)
        self.arm["hand"].increase_rotation(rot)

    def up(self, rot):
        self.arm["shoulder"].increase_rotation(rot)
        self.arm["elbow"].increase_rotation(rot-1)
        self.arm["wrist"].increase_rotation(rot-2)
    
    def down(self, rot):
        self.arm["shoulder"].decrease_rotation(rot)
        self.arm["elbow"].decrease_rotation(rot-1)
        self.arm["wrist"].decrease_rotation(rot-2)

    def mouthOpen(self, rot):
        if self.arm["fingers"].rotation > 72:
            self.arm["fingers"].rotation = 73
        elif self.arm["fingers"].rotation < 11:
            self.arm["fingers"].rotation = 10

        self.arm["fingers"].decrease_rotation(rot)

    def mouthClose(self, rot):
        if self.arm["fingers"].rotation > 72:
            self.arm["fingers"].rotation = 73
        elif self.arm["fingers"].rotation < 11:
            self.arm["fingers"].rotation = 10

        self.arm["fingers"].increase_rotation(rot)        

    def get_packet(self):
        # should create in order (I HOPE)
        packet = b''
        # packet += str.encode('d')
        # packet += bytes([20])
        
        for joint in self.arm.values():
            for b in joint.get_string():
                packet += b

        packet += str.encode("\r")
        # Convert to bytes
        return packet

    
    # def randomize_rotation(self):
    #     #try and keep it safe
    #     for joint in self.arm.values():
    #         num = randint(20, 160)
    #         joint.set_rotation(num)

class Arduino(HardwareAbstractClass):

    def init(self):
        # print ("Arduino init!")
        # print ("running magical things!")
        # arduino = serial.Serial('/dev/cu.usbmodem1441', 9600, timeout=.1)
        try:
            self.arduino  = serial.Serial('/dev/ttyACM0', 115200)
        except:
            print ("Serial not connected!")

        self.start = time.clock()
        self.counter = 0
        self.elapsed_time = 0

        self.arm = Arm()
        self.window = None
        self.connected = False

        self.new_motion = False
        self.new_motion_nn = False
        self.nn_timeout = time.clock()
        self.do_nn = False
        # pass

    def update(self, data):
        # print ("Doing HW things")

        action, nn = data

        bytesToRead = self.arduino.inWaiting()
        rec = self.arduino.read(bytesToRead).decode("utf-8")
        if (rec is not '' and self.window is not None):
            self.window.print("Received: " + rec)
            
        if (not self.connected and "Connect" in rec):
            self.connected = True
            # self.arduino.write(b'm3')
            # print("Beginning program!")
        if (not self.connected):
            return

        if ("mast" in rec or (time.clock() - self.nn_timeout > 10)):
            self.new_motion_nn = False
            print("Disabling nn lock")
            self.arm.reset_arm()

        # print (action)
        if action is not None:
            if (action["Left"]):
                self.arm.left(2)
            if (action["Right"]):
                self.arm.right(2)
            if (action["Up"]):
                self.arm.up(2)
            if (action["Down"]):
                self.arm.down(2)
            if (action["MouthOpen"]):
                self.arm.mouthOpen(10)
            elif (not action["MouthOpen"]):
                self.arm.mouthClose(2)

            self.new_motion = True
            self.nn_timeout = time.clock()

        val = ""
        if nn is not {}:
            if (self.do_nn):
                key = max(nn.items(), key=operator.itemgetter(1))[0]
                if (key is not "neutral" and max(nn.values()) >= _THRESHOLD):
                    # print(key)
                    if (key == "smile"):
                        val = "m3"
                    if (key == "anger"):
                        val = "m1"
                    if (key == "scream"):
                        val = "m2"
                    self.new_motion_nn = True
                    # print("Val: " + val)

        if (self.elapsed_time >= 0.1):
            # print ("Elapsed time: ", self.elapsed_time)
            # print("Current time: ", time.time())
            if (self.new_motion and not self.new_motion_nn):
                self.send_packet()
                self.new_motion = False
            if (self.new_motion_nn):
                self.send_packet(val)
                self.do_nn = False
                
            self.elapsed_time = 0
            self.start = time.clock()
        
        self.elapsed_time += time.clock() - self.start


    def display(self, window):
        self.window = window

    def keyboard(self, key):
        if (key is ' '):
            self.do_nn = True
            print("Ready for neural network!")

    def mouse_click(self, x, y):
        pass

    def send_packet(self, mov=None):

        if (mov is None):
            packet = self.arm.get_packet()
            # packet += "Z"
            # print ("Packet: ", packet)
            # print ("Binary Packet: ", str.encode(packet))

            try:
                self.arduino.write(packet)
                # if (self.window is not None):
                #     self.window.print("Packet sent to Arduino")
                # print('Sent...')
            except:
                print ("Arduino disconnected!")
        
        # Doing NN 
        else:
            try:
                packet = b''
                for c in mov:
                    packet += str.encode(c)
                self.arduino.write(packet)
            except:
                print("Arduino disconnected!")