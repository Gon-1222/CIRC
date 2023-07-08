import json
import os
#from File import Gfile

class Manager():
    __data=[]
    def __init__(self,info):
        self.__data=info
        return

    def read(self):
        return self.__data
