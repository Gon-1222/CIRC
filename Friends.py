import csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json

class friend:
    member=[]
    #読み込み
    def __init__(self):
        JSON_FILE = "service_key.json"
        ID = os.environ["GOOGLE_ID"]

        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
        drive = GoogleDrive(gauth)
        #friendのID：1xsnfiWqE8ZVyEiUjvVsUvZPgcVu0stz6
        #ScheduleのID：1mZQ9kqr_jn_dnDRe6nn3-diblntU1tlU
        file = drive.CreateFile({"id": "1xsnfiWqE8ZVyEiUjvVsUvZPgcVu0stz6", "parents": [{"id": ID}]})
        #file.SetContentString("test")
        #file.Upload()
        data=file.GetContentString()
        print(data)
        print(type(data))
        self.member=json.loads(data)
    #書き込み
    def save(self):
        save= json.dumps(self.member)
        JSON_FILE = "service_key.json"
        ID = os.environ["GOOGLE_ID"]

        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
        drive = GoogleDrive(gauth)
        #friendのID：1xsnfiWqE8ZVyEiUjvVsUvZPgcVu0stz6
        #ScheduleのID：1mZQ9kqr_jn_dnDRe6nn3-diblntU1tlU
        file = drive.CreateFile({"id": "1xsnfiWqE8ZVyEiUjvVsUvZPgcVu0stz6", "parents": [{"id": ID}]})
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
