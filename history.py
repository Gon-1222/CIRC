import json
import os
from File import Gfile

class History():
        __data=[]
        __FILE_ID="1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA"
        def __init__(self,info):
            self.__data=info
            return
        def Add(self,New_data):
            self.__data.insert(0,New_data)
            self.__data.sort(reverse=True)
            #self.save_file(self.__FILE_ID,self.__data)
            return
        def Del(self,Del_data):
            if Del_data in self.__data:
                self.__data.remove(Del_data)
            self.__data.sort(reverse=True)
            #self.save_file(self.__FILE_ID,self.__data)
        def get_last(self):
            return self.__data[0]
