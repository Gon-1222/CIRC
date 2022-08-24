from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
import random, string
class Lazy:
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
        file = drive.CreateFile({"id": "1o7-X7AkZPF_PZucQjm08o28St3vEa0UB", "parents": [{"id": ID}]})
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
        file = drive.CreateFile({"id": "1o7-X7AkZPF_PZucQjm08o28St3vEa0UB", "parents": [{"id": ID}]})
        file.SetContentString(save)
        file.Upload()
        return
    def New(self):
        self.data = [''.join(random.choices(string.ascii_letters + string.digits, k=20))]
        self.save()
        return self.data[0]
    def get_data(self):
        ret = self.data[0]
        self.data=["notallowed"]
        self.save()
        return ret
