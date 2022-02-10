import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
class notify:
    data=[]
    #ロード（コンストラクタ）
    def __init__(self):
        JSON_FILE = "service_key.json"
        ID = os.environ["GOOGLE_ID"]

        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
        drive = GoogleDrive(gauth)
        #friendのID：1xsnfiWqE8ZVyEiUjvVsUvZPgcVu0stz6
        #ScheduleのID：18r7To69SFEYRbOXwuHVoMYTJS4i-2o2U
        #notifyのID:1v9HVTO-w9Cwkoebd-phODpHKIs521lK5
        file = drive.CreateFile({"id": "1v9HVTO-w9Cwkoebd-phODpHKIs521lK5", "parents": [{"id": ID}]})
        #file.SetContentString("test")
        #file.Upload()
        buf=file.GetContentString()
        self.data=json.loads(buf)
    #セーブ
    def save(self):
        save= json.dumps(self.data)
        JSON_FILE = "service_key.json"
        ID = os.environ["GOOGLE_ID"]

        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
        drive = GoogleDrive(gauth)
        #friendのID：1xsnfiWqE8ZVyEiUjvVsUvZPgcVu0stz6
        #ScheduleのID：18r7To69SFEYRbOXwuHVoMYTJS4i-2o2U
        file = drive.CreateFile({"id": "1v9HVTO-w9Cwkoebd-phODpHKIs521lK5", "parents": [{"id": ID}]})
        file.SetContentString(save)
        file.Upload()
    #過去の日付を削除する
    def Clean_Up(self):
        current_dt=datetime.datetime.now()
        Flag=True
        while(Flag):
            Flag=False
            for i in self.data:
                buf = datetime.datetime.strptime(i,'%Y/%m/%d')
                if buf<current_dt:
                    self.data.remove(i)
                    Flag=True
                    break

    #追加
    def Add(self,buf):
        self.data.append(buf)
