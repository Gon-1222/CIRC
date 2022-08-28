import json
import os
import random
import string
from datetime import datetime
from File import Gfile
class Lazy(Gfile):
    __data=[]
    __FILE_ID="1o7-X7AkZPF_PZucQjm08o28St3vEa0UB"

    def __init__(self):
        self.load()
        return

    def load(self):
        self.__data=self.load_file(self.__FILE_ID)
        return

    def save(self):
        print(self.save_file(self.__FILE_ID,self.__data))
        return

    def New(self,number=1):
        self.__data=[''.join(random.choices(string.ascii_letters + string.digits, k=20)) for _ in range(number)]
        self.save()
        return self.__data[-1]

    def check_data(self,token):
        if token in self.__data:
            self.__data.remove(token)
            self.save()
            return True
        return False
