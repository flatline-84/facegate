from abc import ABC, abstractmethod

class ClassifierAbstractClass(ABC):

    """
        Initialize all variables and hardware that might be needed.
        Will get called once at the beginning of the program.

        There will need to be an action map (dict) created that returns a 
        predifined action from an input.
        
        E.G action_map = {  "smile": "wave",
                            "frown": "punch_face"}
    """
    @abstractmethod
    def init(self):
        # print("Overload classifier init function!")
        pass


    """
        This will be used to analyze the data provided in the argument `data` 
        and classify it as an action. 
    """
    @abstractmethod
    def update(self, data):
        # print ("Overload classifier update function!")
        pass

    """
        Returns the action determined from the data input 
        E.G: facial smile = wave, return wave
    """
    @abstractmethod
    def getAction(self):
        # print("Overload classifier data function!")
        pass

    """
        Passes the GUI window into the class to be used to display things. There will be a log and an image viewer.
    """
    @abstractmethod
    def display(self, window):
        pass