from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

class All_Data():
    __ID = os.environ["GOOGLE_ID"]
    __path = os.environ["All_Path"]
    __scope = ["https://www.googleapis.com/auth/drive"]
    __JSON_FILE = "service_key.json"
    data = None
    loaded=0
    def __init__(self):
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.__JSON_FILE, self.__scope)
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({"id": __path, "parents": [{"id": self.__ID}]})
        data=file.GetContentString()
        data = json.loads(data)
        self.loaded=1
        return 0
    def save_file(self):
        if self.loaded==0:
            return False
        contents=json.dumps(data)
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.__JSON_FILE, self.__scope)
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({"id": __path, "parents": [{"id": self.__ID}]})
        file.SetContentString(contents)
        file.Upload()
        return True
