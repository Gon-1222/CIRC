import csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from File import Gfile
import json
import os
class friend(Gfile):
    member=[]
    #読み込み
    def __init__(self):
        self.member=self.load_file("1V6XPVgyb0wudutBfgeuYqUZYYh1ttcx4")
    #書き込み
    def save(self):
        self.member=list(set(self.member))
        self.save_file("1V6XPVgyb0wudutBfgeuYqUZYYh1ttcx4",self.member)
    #追加
    def add(self,IDS):
        self.member.append(IDS)
    #削除
    def remove(self,IDS):
        self.member.remove(IDS)
    #リストを返す
    def LIST(self):
        return self.member
