from abc import ABC, abstractmethod

class HardwareAbstractClass(ABC):

    """
        Initialize all variables and hardware that might be needed.
        Will get called once at the beginning of the program. Will need to have
        same action map as used in the classifier

        E.G initialize serial output with Arduino, wait for response, etc
    """
    @abstractmethod
    def init(self):
        # print("Overload hardware init function!")
        pass


    """
        An `action` will be provided and this will be used to do any 
        calculations needed for the hardware components.
        
        E.G: "wave" is received, move servo arm 20 degrees to the right, then
        send the action to the Arduino
    """
    @abstractmethod
    def update(self, action):
        # print ("Overload classifier update function!")
        pass