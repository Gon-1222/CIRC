import json
import os
import random
import string
from File import Gfile
class Lazy(Gfile):
    __data=[]
    def __init__(self):
        self.load()
        return
    def load(self):
        self.__data=self.load_file("1o7-X7AkZPF_PZucQjm08o28St3vEa0UB")

        return
    def save(self):
        print(self.save_file("1o7-X7AkZPF_PZucQjm08o28St3vEa0UB",self.__data))
        return
    def New(self):
        self.__data.append(''.join(random.choices(string.ascii_letters + string.digits, k=20)))
        self.save()
        return self.__data[-1]
    def check_data(self,token):
        if token in self.__data:
            self.__data.remove(token)
            self.save()
            return True
        return False
