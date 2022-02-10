import csv
import copy
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
import os
class Schedular:
    data=[]
    def __init__(self):
        JSON_FILE = "service_key.json"
        ID = os.environ["GOOGLE_ID"]

        gauth = GoogleAuth()
        scope = ["https://www.googleapis.com/auth/drive"]
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
        drive = GoogleDrive(gauth)
        #friendのID：1xsnfiWqE8ZVyEiUjvVsUvZPgcVu0stz6
        #ScheduleのID：18r7To69SFEYRbOXwuHVoMYTJS4i-2o2U
        file = drive.CreateFile({"id": "18r7To69SFEYRbOXwuHVoMYTJS4i-2o2U", "parents": [{"id": ID}]})
        #file.SetContentString("test")
        #file.Upload()
        buf=file.GetContentString()
        self.data=json.loads(buf)
    #保存
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
        file = drive.CreateFile({"id": "18r7To69SFEYRbOXwuHVoMYTJS4i-2o2U", "parents": [{"id": ID}]})
        file.SetContentString(save)
        file.Upload()
    #データの追加（変更）
    def add(self,userID,datum):
        #元要素削除
        #要素番号とdataの縦軸を回す
        for i,youso in enumerate(self.data):
            #そのデータの0番目の要素とuserIDがあっていたら削除
            if youso[0]==userID:
                self.data.pop(i)
        #datumの1番目に日付の個数
        l=len(datum)
        datum.insert(1,str(l-1))
        #datumの0番目にuserID
        datum.insert(0,userID)
        #dataに追加
        self.data.append(datum)
    #名前と個人個人のスケジュールのリストを返す
    def Schedule_list(self,userID):
        for i in self.data:
            if i[0]==userID:
                i2=copy.deepcopy(i)
                i2.pop(0)#userID
                i2.pop(1)#Noの削除
                return i2
        return [""]
    #各日程の参加メンバーのリスト
    def Member_list(self,date):
        member=[]
        for i,item in enumerate(self.data):
            for j in range(3,int(item[2])+3,1):
                if self.data[i][j]==date:
                    member.append(self.data[i][1])
        return member
    #各日程の参加メンバーの人数
    def count_part(self,date):
        u=self.Member_list(date)
        return len(u)
    #各日程の参加メンバーのリスト（1ヶ月分辞書でまとめて返す）
    def All_lists(self):
        member_dics={}
        #現在の日付の所得
        current_dt=datetime.datetime.now()
        for _ in range(0,30,1):
            #今の日付を文字列に
            current_str=current_dt.strftime('%Y/%m/%d')
            #ディクショナリとして作成
            member_dics[current_str] = self.Member_list(current_str)
            #1日シフト
            current_dt=current_dt+datetime.timedelta(days=1)
        #30日分作って出す
        return member_dics
    #古いデータは消す
    def organize(self):
        current_dt=datetime.datetime.now()
        for i,item in enumerate((self.data)):
            flag=True
            while flag:
                flag=False
                for j in range(3,int(item[2])+3,1):
                    if j>=len(item):break
                    dat=datetime.datetime.strptime(self.data[i][j],'%Y/%m/%d')
                    print(j)
                    if dat<current_dt:
                        del self.data[i][j]
                        self.data[i][2]=str(int(self.data[i][2])-1)
                        flag=True
                        break
