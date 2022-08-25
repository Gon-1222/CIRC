from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

class Gfile():
    __ID = os.environ["GOOGLE_ID"]
    __scope = ["https://www.googleapis.com/auth/drive"]
    __JSON_FILE = "service_key.json"
    def load_file(self,path):
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.__JSON_FILE, self.__scope)
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({"id": path, "parents": [{"id": self.__ID}]})
        data=file.GetContentString()
        return json.loads(data)
    def save_file(self,path,contents):
        if not(isinstance(contents, list) or isinstance(contents, dict)) :
            return False
        contents=json.dumps(contents)
        gauth = GoogleAuth()
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(self.__JSON_FILE, self.__scope)
        drive = GoogleDrive(gauth)
        file = drive.CreateFile({"id": path, "parents": [{"id": self.__ID}]})
        file.SetContentString(contents)
        file.Upload()
        return True
