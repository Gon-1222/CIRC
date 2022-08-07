from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import json
from apiclient import errors
import base64
import csv
import os

# OAuth2.0 Gmail　API用スコープ
# 変更する場合は、token.jsonファイルを削除する

class Mail:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    # アクセストークン取得
    def get_token(self):
        creds = None
        # token.json
        # access/refresh tokenを保存
        # 認可フロー完了時に自動で作成。
        if os.path.exists('/tmp/token.json'):
            creds = Credentials.from_authorized_user_file(
                '/tmp/token.json', self.SCOPES)
        # トークンが存在しない場合
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'creds/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # トークンを保存
            with open('/tmp/token.json', 'w') as token:
                token.write(creds.to_json())
        return creds


    # メールリスト取得
    def get_message_list(self,service, user_id, query, count):
        messages = []
        try:
            message_ids = (
                service.users()
                .messages()
                .list(userId=user_id, maxResults=count, q=query)
                .execute()
            )

            if message_ids["resultSizeEstimate"] == 0:
                print("No DATA")
                return []

            # 各message内容確認
            for message_id in message_ids["messages"]:
                # 各メッセージ詳細
                detail = (
                    service.users()
                    .messages()
                    .get(userId="me", id=message_id["id"])
                    .execute()
                )
                message = {}
                message["id"] = message_id["id"]
                # 本文
                if 'data' in detail['payload']['body']:
                    decoded_bytes = base64.urlsafe_b64decode(
                        detail["payload"]["body"]["data"])
                    decoded_message = decoded_bytes.decode("UTF-8")
                    message["body"] = decoded_message
                else:
                    message["body"] = ""
                # 件名
                message["subject"] = [
                    header["value"]
                    for header in detail["payload"]["headers"]
                    if header["name"] == "Subject"
                ][0]
                # 送信元
                message["from"] = [
                    header["value"]
                    for header in detail["payload"]["headers"]
                    if header["name"] == "From"
                ][0]
                messages.append(message)
            return messages

        except errors.HttpError as error:
            print("An error occurred: %s" % error)
    def read_mail(self,query="is:unread", count=10):
        #最終取得のIDの取得
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
        file = drive.CreateFile({"id": "1ToOKNN6m4y1-gQoHoaZi5dwgmiSu_EUS", "parents": [{"id": ID}]})
            #file.SetContentString("test")
            #file.Upload()
        buf=file.GetContentString()
        Last_ID=json.loads(buf)
            # 1. アクセストークン取得
        creds = self.get_token()
            # 2. Gmail API (メッセージ一覧取得) 呼び出し
        service = build('gmail', 'v1', credentials=creds)
        messages = self.get_message_list(service, "me", query,
                            count=count)
        if messages:
            if messages[0]["id"]!=Last_ID:
                save= json.dumps(messages[0]["id"])
                JSON_FILE = "service_key.json"
                ID = os.environ["GOOGLE_ID"]
                gauth = GoogleAuth()
                scope = ["https://www.googleapis.com/auth/drive"]
                gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)
                drive = GoogleDrive(gauth)
                file = drive.CreateFile({"id": "1ToOKNN6m4y1-gQoHoaZi5dwgmiSu_EUS", "parents": [{"id": ID}]})
                file.SetContentString(save)
                file.Upload()
                return_data=[]
                for i in messages:
                    if i["id"]==Last_ID:
                        break
                    return_data.append(i["subject"])
                return return_data
            else:
                return None
        else:
            return None


if __name__ == '__main__':
    a=Mail()
    print(a.read_mail())
