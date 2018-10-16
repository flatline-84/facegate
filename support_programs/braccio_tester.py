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

_BUF_SIZE = 15

# # Sequence 1 - Pick up/put down
# Braccio.ServoMovement(20, 0, 45, 55, 45, 90, 10); // Bend
# to
# pick
# up
# delay(500);
# Braccio.ServoMovement(10, 0, 45, 55, 45, 90, 73); // Close
# Claw
# delay(500);
# Braccio.ServoMovement(20, 180, 90, 55, 90, 90, 73);
# delay(500);
# Braccio.ServoMovement(20, 180, 45, 55, 45, 90, 73);
# delay(500);
# Braccio.ServoMovement(20, 180, 45, 55, 45, 90, 10);

# delay(1000);
# Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 73);

# Sequence 2 - Door Handle
# Braccio.ServoMovement(20, 0, 45, 55, 45, 90, 10); // Bend
# to
# pick
# up
# delay(500);
# Braccio.ServoMovement(10, 90, 45, 90, 45, 90, 10); // Claw open
# Claw
# delay(500);
# Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 73); // Close Claw
# delay(500);
# Braccio.ServoMovement(20, 90, 45, 55, 45, 180, 73); // Rotate Claw
# delay(500);
# Braccio.ServoMovement(20, 90, 45, 55, 45, 180, 10); // Open Claw

# delay(1000);
# Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 73); // Reset

# Sequence 3 - Wave
# Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 73); // Bend
# to
# pick
# up
# delay(500);
# Braccio.ServoMovement(10, 0, 45, 90, 90, 90, 10); // Claw open
# Claw
# delay(500);
# Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 10); //  Up claw open
# delay(500);
# Braccio.ServoMovement(20, 90, 60, 80, 80, 90, 10); // To the side
# delay(100);
# Braccio.ServoMovement(20, 90, 120, 100, 100, 90, 10); // Other side
# delay(100);
# Braccio.ServoMovement(20, 90, 60, 80, 80, 90, 10); // To the side
# delay(100);
# Braccio.ServoMovement(20, 90, 120, 100, 100, 90, 10); // Other side
# delay(100);
# Braccio.ServoMovement(20, 90, 45, 55, 45, 180, 10); //

# delay(1000);
# Braccio.ServoMovement(20, 90, 90, 90, 90, 90, 73); // Reset




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
        return [str.encode(self.uniq_char), bytes([self.rotation])]


class Arm:
    def __init__(self):
        self.arm = {
            "base":     Joint("base", 'b'),
            "shoulder": Joint("shoulder", 's'),
            "elbow":    Joint("elbow", 'e'),
            "wrist":    Joint("wrist", 'w'),
            "hand":    Joint("hand", 'h'),
            "fingers":  Joint("fingers", 'f')
        }
    def get_packet(self):
        # should create in order (I HOPE)
        packet = b''
        for joint in self.arm.values():
            for b in joint.get_string():
                packet += b
        packet += str.encode("\r")
        # Convert to bytes
        return packet
    
    def randomize_rotation(self):
        #try and keep it safe
        for joint in self.arm.values():
            num = randint(20, 160)
            joint.set_rotation(num)

    

if __name__ == '__main__':

    if (len(sys.argv) == 1):
        _DEBUG = True
    elif (len(sys.argv) == 2):
        _DEBUG = False
    else:
        print("Too few or too many arguments! Insure you are only passing the Arduino port")
        print("Eg: /dev/ttyUSB0")
        exit(1)

    if (not _DEBUG):
        arduino = serial.Serial()
        arduino.port = sys.argv[1]
        print(sys.argv[1])
        arduino.baudrate = 115200

        # Check that it connects to the Arduino
        while (not arduino.is_open):
            arduino.open()
            print("Trying to connect to Arduino...")
            time.sleep(2)
        print("Connected to Arduino!")

    arm = Arm()
    print("Initial packet: ", arm.get_packet())

    connected = False

    while(True):
        bytesToRead = arduino.inWaiting()
        rec = arduino.read(bytesToRead).decode("utf-8")
        if (rec is not ''):
            print("Received: " + rec)
        
        if (not connected and "Connect" in rec):
            connected = True
            arduino.write(b'm3')
            print("Beginning program!")
        if (not connected):
            continue

        packet = arm.get_packet()
        print("Sending packet: ", (packet))
        if (not _DEBUG): arduino.write(packet)
        arm.randomize_rotation()
        Change this if it's too slow / fast
        time.sleep(5)
        if (not _DEBUG): arduino.write(b'm2')
        time.sleep(5)