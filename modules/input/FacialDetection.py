from ..abstract.InputAbstract import InputAbstractClass

class FacialDetection(InputAbstractClass):

    def init(self):
        print ("Facial Detection!")

    def update(self):
        print ("Facial update")

    def getData(self):
        print ("Facial get data!")
        return [10,20,39,12]