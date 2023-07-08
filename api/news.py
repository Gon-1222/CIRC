import json
import os
#from File import Gfile

class News():
    data=[]
    def __init__(self,info):

        self.data=info

        return
    #def save(self):
        #self.save_file("18fXj0_xqNWWXPGkEYB1dtJLvpMr4kuz4",self.data)
        #return
    def Change(self,naiyou):
        self.data[0]=naiyou
        return
    def get_data(self):
        return self.data[0]
