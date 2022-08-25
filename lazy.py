import json
import os
import random
import string
from File import Gfile
import time
class Lazy(Gfile):
    data=[]
    def __init__(self):
        self.load()
        return
    def load(self):
        self.data=self.load_file("1o7-X7AkZPF_PZucQjm08o28St3vEa0UB")

        return
    def save(self):
        self.save_file("1o7-X7AkZPF_PZucQjm08o28St3vEa0UB",self.data)
        return
    def New(self):
        self.data = [''.join(random.choices(string.ascii_letters + string.digits, k=20))]
        print(self.save())
        print(self.data)
        print(time.perf_counter())
        return self.data[0]
    def get_data(self):
        print("data:",self.data[0])
        print(time.perf_counter())
        ret = self.data[0]
        self.data=["notallowed"]
        self.save()
        return ret
