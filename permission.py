import hashlib
import os
import json
import bcrypt
from File import Gfile

class permit(Gfile):
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
            self.data=self.load_file("1LuFlOw0Axk4r7lyexB6lj1gBzTXm9WOn")
            self.loaded+=1
        if mode&2 and not(self.loaded&2):
            #リクエストの読み込み
            self.req=self.load_file("1XV0OsI7uJDFfsyLnKVVQP69kn2XOFEFI")
            self.loaded+=2
        return
    #保存
    def save(self):
        if self.loaded==0:
            return
        if self.loaded&1:
            self.save_file("1LuFlOw0Axk4r7lyexB6lj1gBzTXm9WOn",self.data)
            #現在マネージャーの書き込み
        if self.loaded&2:
            #リクエストの書き込み
            self.save_file("1XV0OsI7uJDFfsyLnKVVQP69kn2XOFEFI",self.req)
        return
    #管理者追加リクエスト
    def Apply(self,user,password):
        if not(self.loaded&2):
            self.load(2)
        password_hash=bcrypt.hashpw(password.encode(),bcrypt.gensalt(rounds=10,prefix=b'2b')).decode()
        add_data={user:password_hash}
        self.req.update(add_data)
        self.save()
        return "Success"
    #許可リクエスト
    def Allow(self,user):
        if not(self.loaded&3):
            self.load(3)
        print(user)
        print(self.req)
        if user in self.req:
            print(self.req)
            self.data.update({user:self.req[user]})
            self.req.pop(user)
            self.save()
            return "Success"
        else:
            return "Not Found the user"
    #削除
    def Del(self,user):
        if not(self.loaded&1):
            self.load(1)
        if user in self.data:
            self.data.pop(user)
            self.save()
            return "Success"
        else:
            return "Not Found the user"
    #管理者ログインチェック
    def Check(self,user,password):
        if user=="" or password=="":
            return False
        if not(self.loaded&1):
            self.load(1)
        if self.data.get(user):
            return bcrypt.checkpw(password.encode(),self.data[user].encode())
        return False
    #管理者リスト
    def User_lists(self):
        if not(self.loaded&3):
            self.load(3)
        return [self.data,self.req]
