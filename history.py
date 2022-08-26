import json
import os
from File import Gfile

class History(Gfile):
        __data=[]
        __FILE_ID="1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA"
        def Add(self,New_data):
            self.__data=self.load_file(__FILE_ID)
            self.__data.insert(0,New_data)
            self.save_file(__FILE_ID,self.__data)
            return
        def Del(self,Del_data):
            self.__data=self.load_file(__FILE_ID)
            if Del_data in self.__data:
                self.__data.remove(Del_data)
            self.save_file(__FILE_ID,self.__data)
