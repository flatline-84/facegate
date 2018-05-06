from ..abstract.HardwareAbstract import HardwareAbstractClass

class Arduino(HardwareAbstractClass):
    
    def init(self):
        print ("Arduino init!")

    def update(self, action):
        print ("Doing HW things")