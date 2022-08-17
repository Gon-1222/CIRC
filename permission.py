#pydrive関係とファイルIOもかく
import hashlib
import os
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import bcrypt
class permit:
    data={}
    req={}
    loaded=0
    #mode=0:not allowed
    #mode=1:現在マネージャーのみ
    #mode=2:リクエストのみ
    #mode=3:全て読込
    def __init__(self,mode=0):
        self.load(mode)
        return
    #読み込み
    def load(self,mode):
        if mode==0:
            return
        if mode&1 and not(self.loaded&1):
            #現在マネージャーの読み込み
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
            file = drive.CreateFile({"id": "1LuFlOw0Axk4r7lyexB6lj1gBzTXm9WOn", "parents": [{"id": ID}]})
            #file.SetContentString("test")
            #file.Upload()
            buf=file.GetContentString()
            self.data=json.loads(buf)
            self.loaded+=1
        if mode&2 and not(self.loaded&2):
            #リクエストの読み込み
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
            file = drive.CreateFile({"id": "1XV0OsI7uJDFfsyLnKVVQP69kn2XOFEFI", "parents": [{"id": ID}]})
            #file.SetContentString("test")
            #file.Upload()
            buf=file.GetContentString()
            self.req=json.loads(buf)
            self.loaded+=2
        return
    #保存
    def save(self):
        if self.loaded==0:
            return
        if self.loaded&1:
            save= json.dumps(self.data)
            gauth = GoogleAuth()
            scope = ["https://www.googleapis.com/auth/drive"]
            gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
            drive = GoogleDrive(gauth)
            file = drive.CreateFile({"id": "1LuFlOw0Axk4r7lyexB6lj1gBzTXm9WOn", "parents": [{"id": ID}]})
            file.SetContentString(save)
            file.Upload()
            #現在マネージャーの書き込み
        if self.loaded&2:
            #リクエストの書き込み
            save= json.dumps(self.req)
            gauth = GoogleAuth()
            scope = ["https://www.googleapis.com/auth/drive"]
            gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
            drive = GoogleDrive(gauth)
            file = drive.CreateFile({"id": "1XV0OsI7uJDFfsyLnKVVQP69kn2XOFEFI", "parents": [{"id": ID}]})
            file.SetContentString(save)
            file.Upload()
        return
    #管理者追加リクエスト
    def Apply(self,user,passeord):
        if not(self.loaded&2):
            self.load(2)
        password_hash=bcrypt.hashpw(password,bcrypt.gensalt(rounds=14,prefix=b'2b')).decode()
        add_data={user:password_hash}
        self.req.update(add_data)
        self.save(2)
        return "Success"
    #許可リクエスト
    def Allow(self,user):
        if not(self.loaded&3):
            self.load(3)
        if user in self.req:
            self.data.update({user:self.req[user]})
            self.req.pop(user)
            self.save(3)
            return "Success"
        else:
            return "Not Found the user"
    #削除
    def Del(self,user):
        if not(self.loaded&1):
            self.load(1)
        if user in self.data:
            self.data.pop(user)
            self.save(1)
            return "Success"
        else:
            return "Not Found the user"
    #管理者ログインチェック
    def Check(self,user,password):
        if not(self.loaded&1):
            self.load(1)
        return bcrypt.checkpw(password.encode(),self.data.get(user,""))
    #管理者リスト
    def User_lists(self):
        if not(self.loaded&3):
            self.load(3)
        return self.data,self.req
