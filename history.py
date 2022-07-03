from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
class History:
        data=[]
        def __init__(self,New_data):
            JSON_FILE = "service_key.json"
            ID = os.environ["GOOGLE_ID"]
            gauth = GoogleAuth()
            scope = ["https://www.googleapis.com/auth/drive"]
            gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
            drive = GoogleDrive(gauth)
            #friendのID：1xsnfiWqE8ZVyEiUjvVsUvZPgcVu0stz6
            #ScheduleのID：18r7To69SFEYRbOXwuHVoMYTJS4i-2o2U
            #notifyのID:1v9HVTO-w9Cwkoebd-phODpHKIs521lK5
            file = drive.CreateFile({"id": "1j2Bj9bNyk8h2x-QShdDl7-wqxdT732vY", "parents": [{"id": ID}]})
            #file.SetContentString("test")
            #file.Upload()
            buf=file.GetContentString()
            self.data=json.loads(buf)
            self.data.insert(0,New_data)
            self.data.pop(3)
            save= json.dumps(self.data)
            gauth = GoogleAuth()
            scope = ["https://www.googleapis.com/auth/drive"]
            gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
            drive = GoogleDrive(gauth)
            #friendのID：1xsnfiWqE8ZVyEiUjvVsUvZPgcVu0stz6
            #ScheduleのID：18r7To69SFEYRbOXwuHVoMYTJS4i-2o2U
            file = drive.CreateFile({"id": "1j2Bj9bNyk8h2x-QShdDl7-wqxdT732vY", "parents": [{"id": ID}]})
            file.SetContentString(save)
            file.Upload()
