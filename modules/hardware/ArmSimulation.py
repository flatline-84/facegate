from ..abstract.HardwareAbstract import HardwareAbstractClass

import tkinter as tk
import math

class ArmComponent():
    def __init__(self, x, y, rotation, size_x, size_y):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.size_x = size_x
        self.size_y = size_y
        self.mid_x = x + (size_x / 2)
        self.mid_y = y + (size_y / 2)

        # Each point of the rectangle, will be calculated using rotation
        #   4   +---+   1
        #       | o |
        #   3   +---+   2

        self.vertices = [
            [self.mid_x + (self.size_x / 2), self.mid_y + (self.size_y / 2)],
            [self.mid_x + (self.size_x / 2), self.mid_y - (self.size_y / 2)],
            [self.mid_x - (self.size_x / 2), self.mid_y - (self.size_y / 2)],
            [self.mid_x - (self.size_x / 2), self.mid_y + (self.size_y / 2)],
        ]

        self.points = []
        self.window = None

    def increase_rotation(self, num):
        self.rotation += num
        if (self.rotation > 180):
            self.rotation = 180

    def decrease_rotation(self, num):
        self.rotation -= num
        if (self.rotation < 0):
            self.rotation = 0


    def calculate_vertices(self):
        angle = math.radians(self.rotation)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
    
        def _rot(x, y):
            x -= self.x
            y -= self.y
            _x = x * cos_val + y * sin_val
            _y = -x * sin_val + y * cos_val
            return _x + self.x, _y + self.y

        for i in range(len(self.vertices)):
            self.vertices[i] = _rot(self.vertices[i][0], self.vertices[i][1])

        

    def update_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, window):
        if (self.window == None):
            self.window = window

        if (len(self.points) == 0):
            for i in range(len(self.vertices) - 1):
                self.points.append(self.window.canvas.create_line(self.vertices[i][0], self.vertices[i][1], self.vertices[i+1][0], self.vertices[i+1][1], fill="blue", width=2))
            
        for i in range(len(self.points)):
                self.window.canvas.coords(self.points[i], self.vertices[i][0], self.vertices[i][1] , self.vertices[i+1][0] , self.vertices[i+1][1])
    
class Arm():
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


    def __init__(self, pos_x, pos_y):
        self.components = {
                                        # x, y, rot, sx, sy
            'base'      : ArmComponent(0+pos_x, 0+pos_y, 0, 0, 0),
            'shoulder'  : ArmComponent(0+pos_x, 0+pos_y, 0, 0, 0),
            'elbow'     : ArmComponent(0+pos_x, 0+pos_y, 0, 0, 0),
            'wrist'     : ArmComponent(0+pos_x, 0+pos_y, 0, 0, 0),
            'fingers'   : ArmComponent(0+pos_x, 0+pos_y, 0, 0, 0)
        }

class ArmSimulation(HardwareAbstractClass):

    def init(self):
        # print("Overload hardware init function!")
        self.window = None
        self.data = None
        # self.points = []
        # self.offset = -100
        self.offset = 0

    def update(self, action):
        # print ("Overload classifier update function!")
        self.data = action

    def display(self, window):
        if (self.window == None):
            self.window = window
        else:
            # print(self.data)
            pass

        if (len(self.points) == 0):
            # print(len(self.data))
            for i in range(len(self.data) - 1):
                self.points.append(self.window.canvas.create_line(self.data[i][0] + self.offset, self.data[i][1] , self.data[i+1][0] + self.offset, self.data[i+1][1], fill="blue", width=2))
                print( self.data[i])
            print (len(self.points))

        #Update face
        elif (len(self.data) >0):
            for i in range(len(self.points)):
                self.window.canvas.coords(self.points[i], self.data[i][0] + self.offset, self.data[i][1] , self.data[i+1][0] + self.offset, self.data[i+1][1]) 
                # change coordinates


    def keyboard(self, key):
        pass

    def mouse_click(self, x, y):
        pass