from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
class History:
        data=[]
        def Add(self,New_data):
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
            file = drive.CreateFile({"id": "1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA", "parents": [{"id": ID}]})
            #file.SetContentString("test")
            #file.Upload()
            buf=file.GetContentString()
            self.data=json.loads(buf)
            self.data.insert(0,New_data)
            save= json.dumps(self.data)
            gauth = GoogleAuth()
            scope = ["https://www.googleapis.com/auth/drive"]
            gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
            drive = GoogleDrive(gauth)
            file = drive.CreateFile({"id": "1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA", "parents": [{"id": ID}]})
            file.SetContentString(save)
            file.Upload()
        def Del(self,Del_data):
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
            file = drive.CreateFile({"id": "1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA", "parents": [{"id": ID}]})
            #file.SetContentString("test")
            #file.Upload()
            buf=file.GetContentString()
            self.data=json.loads(buf)
            self.data.remove(Del_data)
            save= json.dumps(self.data)
            gauth = GoogleAuth()
            scope = ["https://www.googleapis.com/auth/drive"]
            gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
            drive = GoogleDrive(gauth)
            file = drive.CreateFile({"id": "1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA", "parents": [{"id": ID}]})
            file.SetContentString(save)
            file.Upload()
