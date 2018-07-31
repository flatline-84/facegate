from ..abstract.HardwareAbstract import HardwareAbstractClass

class FaceSimulation(HardwareAbstractClass):

    def init(self):
        # print("Overload hardware init function!")
        self.window = None
        self.data = None
        self.points = []
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