import json
import os
import random
import string
from datetime import datetime
#from File import Gfile
class Lazy():
    __data=[]
    __FILE_ID="1o7-X7AkZPF_PZucQjm08o28St3vEa0UB"

    def __init__(self,info):
        self.__data = info
        return



    #def save(self):
        #print(self.save_file(self.__FILE_ID,self.__data))
    #    return

    def New(self,number=1):

        self.__data.append(''.join(random.choices(string.ascii_letters + string.digits, k=20)))
        print(id(self.__data))
        print(self.__data)
        #self.save()
        return self.__data[-1]

    def check_data(self,token):
        if token in self.__data:
            self.__data.remove(token)
            #self.save()
            return True
        return False
