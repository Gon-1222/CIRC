import json
import os
from File import Gfile

class Manager(Gfile):
    __data=[]
    def __init__(self):
        self.__data=self.load_file("1o6aBXBzo3QpF7rCYICHaS4SKffxOfkum")
        return

    def read(self):
        return self.__data
