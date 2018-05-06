from ..abstract.ClassifierAbstract import ClassifierAbstractClass

class FaceClassifier(ClassifierAbstractClass):

    def init(self):
        print ("Face classifier init!")
        #,data
    def update(self, data):
        print ("Face classifier update!")

    def getAction(self):
        print ("Face classifier action")
        return "wave"