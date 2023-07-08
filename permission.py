import hashlib
import os
import json
import bcrypt
#from File import Gfile

class permit():
    __data={}
    __req={}
    loaded=0
    #mode=0:not allowed
    #mode=1:現在マネージャーのみ
    #mode=2:リクエストのみ
    #mode=3:全て読込
    def __init__(self,mode=0,info=""):
        if mode==0:
            return
        if mode&1 and not(self.loaded&1):
            self.__data=info["permission"]
            self.loaded+=1
        if mode&2 and not(self.loaded&2):
            #リクエストの読み込み
            self.__req=info["req_permit"]
            self.loaded+=2
        return

    #読み込み
    #管理者追加リクエスト
    def Apply(self,user,password):
        if not(self.loaded&2):
            self.load(2)
        password_hash=bcrypt.hashpw(password.encode(),bcrypt.gensalt(rounds=10,prefix=b'2b')).decode()
        add_data={user:password_hash}
        self.__req.update(add_data)
        self.save()
        return "Success"
    #許可リクエスト
    def Allow(self,user):
        if not(self.loaded&3):
            self.load(3)
        print(user)
        print(self.__req)
        if user in self.__req:
            print(self.__req)
            self.__data.update({user:self.__req[user]})
            self.__req.pop(user)
            self.save()
            return "Success"
        else:
            return "Not Found the user"
    #削除
    def Del(self,user):
        if not(self.loaded&1):
            self.load(1)
        if user in self.__data:
            self.__data.pop(user)
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
        if self.__data.get(user):
            return bcrypt.checkpw(password.encode(),self.__data[user].encode())
        return False
    #管理者リスト
    def User_lists(self):
        if not(self.loaded&3):
            self.load(3)
        return [self.__data,self.__req]
