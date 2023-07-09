#from File import Gfile
import json
import os

class friend():
    member=[]
    #読み込み
    def __init__(self,info):
        self.member=info
    #書き込み
    def save(self):
        self.member=list(set(self.member))
        #self.save_file("1V6XPVgyb0wudutBfgeuYqUZYYh1ttcx4",self.member)
    #追加
    def add(self,IDS):
        self.member.append(IDS)
    #削除
    def remove(self,IDS):
        while (IDS in self.member):
            self.member.remove(IDS)
    #リストを返す
    def LIST(self):
        return self.member

    def RESET(self):
        while(self.member!=[]):
            self.member.pop(0)
