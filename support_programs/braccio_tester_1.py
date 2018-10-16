""" Instructions 

Requirements: 
    * Arduino IDE (is it an IDE? I have no idea)
    * install the braccio library through the library manager
    * pyserial Python library (should already be installed for you)

Steps:
    1. Build and flash ../arduino/robot_arm.ino to the Braccio Arduino board
    2. Keep it connected to your PC
    3. Run this program while the braccio is still powered off (maybe?)
    4. Provide the USB device as an argument to this program (no flags)

Notes:
    * baud rate is 9600
"""

# XXXX  XXXX
# XX      XX
# XX+----+XX
# XX| O  |XX
#   Fingers
#   |    |             +-------+
#  +------------------------+  |
#  || O  |     Wrist   |  O |  |
#  +------------------------+  |
#                      |       |
#                      | Elbow |
#                      |       |
#                      |       |
#                      |       |
#                  +---------------+
#                  |   |   O   |   |
#                  |   +-------+   |
#                  |               |
#                  |     Shoulder  |
#           +------------------------------+
#           |              O               |
#           |             Base             |
#           +------------------------------+

# Each named box corresponds to a component
# Each 'O' represents a hinge / rotation point 
# This model corresponds to the physical orange one

import sys
import serial
import time
from random import randint

_DEBUG = False

class Joint:                 #char to be used in packet 
    def __init__(self, nome, uniq_char):
        self.name = nome
        self.rotation = 90
        self.uniq_char = uniq_char
    def set_rotation(self, rot):
        if (rot > 180):
            rot = 180
        if (rot < 0):
            rot = 0
        self.rotation = rot
    def get_string(self):
        return self.uniq_char + str(self.rotation)


class Arm:
    def __init__(self):
        self.arm = {
            "base":     Joint("base", 'b'),
            "shoulder": Joint("shoulder", 's'),
            "elbow":    Joint("elbow", 'e'),
            "wrist":    Joint("wrist", 'w'),
            "fingers":  Joint("fingers", 'f')
        }
    def get_packet(self):
        # should create in order (I HOPE)
        packet = ""
        for joint in self.arm.values():
            packet += joint.get_string()
        packet += "\r"
        # Convert to bytes
        return str.encode(packet)
    
    def randomize_rotation(self):
        #try and keep it safe
        for joint in self.arm.values():
            num = randint(20, 90)
            joint.set_rotation(num)

    

if __name__ == '__main__':

    if (len(sys.argv) != 2):
        print("Too few or too many arguments! Insure you are only passing the Arduino port")
        print("Eg: /dev/ttyUSB0")
        exit(1)

    if (not _DEBUG):

        arduino=serial.Serial(sys.argv[1],9600)

	# Check that it connects to the Arduino
        while (not arduino.is_open):
            arduino.open()
            print("Trying to connect to Arduino...")
            time.sleep(2)
        print("Connected!")

    arm = Arm()
    print("Initial packet: ", arm.get_packet())

    while(True):
        packet = arm.get_packet()
        print("Sending packet: ", packet)
        if (not _DEBUG): arduino.write(packet)
        arm.randomize_rotation()
        # Change this if it's too slow / fast
        time.sleep(1)
