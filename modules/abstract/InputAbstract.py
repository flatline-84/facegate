from abc import ABC, abstractmethod

class InputAbstractClass(ABC):

    """
        Initialize all variables and hardware that might be needed.
        Will get called once at the beginning of the program.
    """
    @abstractmethod
    def init(self):
        # print("Overload input init function!")
        pass


    """
        This will be used to read data from the input device and do any 
        calculations necessary. 

        Face example: read an image from the camera, analyze the image, find the
        face, get coordinate points of features
    """
    @abstractmethod
    def update(self):
        # print ("Overload input update function!")
        pass

    """
        Returns the data collected from update() with any transformations 
        applied. E.g normalizing coordinate points
    """
    @abstractmethod
    def getData(self):
        # print("Overload input data function!")
        pass

    """
        Passes the GUI window into the class to be used to display things. There will be a log and an image viewer.
    """
    @abstractmethod
    def display(self, window):
        pass

    """
        Triggers when there is  a keyboard press.
    """
    @abstractmethod
    def keyboard(self, key):
        pass

    """
        Returns coordinates of where there is a mouse click
    """
    @abstractmethod
    def mouse_click(self, x, y):
        pass