from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
class Manager:
    data=[]
    def __init__(self):
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
                #lastmailのID：1ToOKNN6m4y1-gQoHoaZi5dwgmiSu_EUS
                #managerのID：1o6aBXBzo3QpF7rCYICHaS4SKffxOfkum
        file = drive.CreateFile({"id": "1o6aBXBzo3QpF7rCYICHaS4SKffxOfkum", "parents": [{"id": ID}]})
            #file.SetContentString("test")
            #file.Upload()
        buf=file.GetContentString()
        self.data=json.loads(buf)
        return

    def read(self):
        return self.data
