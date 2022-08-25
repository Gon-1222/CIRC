import json
import os
from File import Gfile

class News(Gfile):
    data=[]
    def __init__(self):
        self.load()
        return
    def load(self):
        self.data=self.load_file("18fXj0_xqNWWXPGkEYB1dtJLvpMr4kuz4")
        return
    def save(self):
        self.save_file("18fXj0_xqNWWXPGkEYB1dtJLvpMr4kuz4",self.data)
        return
    def Change(self,naiyou):
        self.data[0]=naiyou
        self.save()
        return
    def get_data(self):
        return self.data[0]
