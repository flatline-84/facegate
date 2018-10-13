import pyforms
from   pyforms          import BaseWidget
from   pyforms.controls import ControlText
from   pyforms.controls import ControlButton
from pyforms.controls import ControlImage

import cv2
class SimpleExample1(BaseWidget):

    def __init__(self):
        super(SimpleExample1,self).__init__("FaceGate")
        # self.visible = True
        self.set_margin (300)

        self.formset = [ ('_firstname','_middlename','_lastname'), '_button', '_fullname', ' _image',' ']
        # self.formset = [ {
        #     'Tab1':['_firstname','||','_middlename','||','_lastname'], 
        #     'Tab2': ['_fullname']
        #     },
        #    '=',(' ','_button', ' ') ]
        #Use dictionaries for tabs
        #Use the sign '=' for a vertical splitter
        #Use the signs '||' for a horizontal splitter

        #Definition of the forms fields
        self._firstname     = ControlText('First name', 'Default value')
        self._middlename    = ControlText('Middle name')
        self._lastname      = ControlText('Lastname name')
        self._fullname      = ControlText('Full name')
        self._button        = ControlButton('Press this button')

        self._image = ControlImage()

        self.run()

        # #Define the button action
        # self._button.value = self.__buttonAction

    # def __buttonAction(self):
    #     """Button action event"""
    #     self._fullname.value = self._firstname.value +" "+ self._middlename.value + \
    #     " "+ self._lastname.value
    def run(self):
        self._image.value = 'numbered.jpg'
        self._image.repaint()

#Execute the application
if __name__ == "__main__":   
    pyforms.start_app( SimpleExample1 )
