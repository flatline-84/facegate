from ..abstract.HardwareAbstract import HardwareAbstractClass

class FaceSimulation(HardwareAbstractClass):

    def init(self):
        # print("Overload hardware init function!")
        self.window =       None
        self.data =         None
        self.points =       []
        # self.offset = -100
        self.offset =       0

        # self.actions = {
        #     "MouthOpen":    False,
        #     "Left":         False,
        #     "Right":        False,
        #     "Up":           False,
        #     "Down":         False
        # }

        self.text_title =   None
        self.text_body =    None

        # For drawing text on the window
        self.x =            440
        self.y =            60
        self.dy =           30

    def update(self, params):
        # print (params)
        self.data, self.actions = params

    def display(self, window):
        text_str = ""

        for key, value in self.actions.items():
            if (value):
                text_str += key + "\n"

        if (self.window is None):
            self.window = window

        if (self.text_title is None):
            self.text_title = self.window.canvas.create_text(self.x, self.y, anchor="nw")
            self.window.canvas.itemconfig(self.text_title, text="Actions", font=("Helvetica", 22, "bold"), fill="purple")
        if (self.text_body is None):
            self.text_body = self.window.canvas.create_text(self.x, self.y + self.dy, anchor="nw")
            self.window.canvas.itemconfig(self.text_body, font=("Helvetica", 18), fill="blue")
        else:
            self.window.canvas.itemconfig(self.text_body, text=text_str)

        for key, value in self.actions.items():
            text_str = ""
            if (value):
                text_str += key + "\n"
        
        if (len(self.points) == 0):
            # print(len(self.data))
            if (len(self.data) > 0):
                print(self.data)
                for i in range(len(self.data) - 1):
                    self.points.append(self.window.canvas.create_line(self.data[i][0] + self.offset, self.data[i][1] , self.data[i+1][0] + self.offset, self.data[i+1][1], fill="blue", width=2))
                    print( self.data[i])
                print (len(self.points))

        #Update face
        elif (len(self.data) > 0):
            for i in range(len(self.points)):
                self.window.canvas.coords(self.points[i], self.data[i][0] + self.offset, self.data[i][1] , self.data[i+1][0] + self.offset, self.data[i+1][1]) 
                # change coordinates

    def keyboard(self, key):
        pass

    def mouse_click(self, x, y):
        pass