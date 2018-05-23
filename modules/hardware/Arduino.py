from ..abstract.HardwareAbstract import HardwareAbstractClass

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
