from ..abstract.InputAbstract import InputAbstractClass

class FacialDetection(InputAbstractClass):

    def init(self):
        # print ("Facial Detection!")
        pass

    def update(self):
        # print ("Facial update")
        pass

    def getData(self):
        # print ("Facial get data!")
        return [10,20,39,12]

    def display(self, window):
        window.print("Yo mama")
        pass