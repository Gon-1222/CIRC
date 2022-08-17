from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

class News:
    data=[]
    def __init__(self):
        self.load()
        return
    def load(self):
        JSON_FILE = "service_key.json"
        ID = os.environ["GOOGLE_ID"]
        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
        drive = GoogleDrive(gauth)
        #historyのID： 1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA
        #notifyのID：1nS6ug9PSR5QNN8iWism-oRn-HZvyQPL-
        #friendsのID：1V6XPVgyb0wudutBfgeuYqUZYYh1ttcx4
        #sheduleのID：1ppdSzlPtyQWKh3_dTGbvyNlNdUYd5XZ8
        file = drive.CreateFile({"id": "18fXj0_xqNWWXPGkEYB1dtJLvpMr4kuz4", "parents": [{"id": ID}]})
        #file.SetContentString("test")
        #file.Upload()
        buf=file.GetContentString()
        self.data=json.loads(buf)
        return
    def save(self):
        save= json.dumps(self.data)
        JSON_FILE = "service_key.json"
        ID = os.environ["GOOGLE_ID"]
        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({"id": "18fXj0_xqNWWXPGkEYB1dtJLvpMr4kuz4", "parents": [{"id": ID}]})
        file.SetContentString(save)
        file.Upload()
        return
    def Change(self,naiyou):
        self.data=naiyou
        self.save()
        return
    def get_data(self):
        return self.data
