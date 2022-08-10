import csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
class friend:
    ID = os.environ["GOOGLE_ID"]
    scope = ["https://www.googleapis.com/auth/drive"]
    member=[]
    #読み込み
    def __init__(self):
        JSON_FILE = "service_key.json"
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, self.scope)
        drive = GoogleDrive(gauth)
            #historyのID： 1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA
            #notifyのID：1nS6ug9PSR5QNN8iWism-oRn-HZvyQPL-
            #friendsのID：1V6XPVgyb0wudutBfgeuYqUZYYh1ttcx4
            #sheduleのID：1ppdSzlPtyQWKh3_dTGbvyNlNdUYd5XZ8
        file = drive.CreateFile({"id": "1V6XPVgyb0wudutBfgeuYqUZYYh1ttcx4", "parents": [{"id": self.ID}]})
        #file.SetContentString("test")
        #file.Upload()
        data=file.GetContentString()
        self.member=json.loads(data)
    #書き込み
    def save(self):
        self.member=list(set(self.member))
        save= json.dumps(self.member)
        JSON_FILE = "service_key.json"
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, self.scope)
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({"id": "1V6XPVgyb0wudutBfgeuYqUZYYh1ttcx4", "parents": [{"id": self.ID}]})
        file.SetContentString(save)
        file.Upload()
    #追加
    def add(self,IDS):
        self.member.append(IDS)
    #削除
    def remove(self,IDS):
        self.member.remove(IDS)
    #リストを返す
    def LIST(self):
        return self.member
