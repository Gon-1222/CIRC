import hashlib
import os
import json
import bcrypt
from linebot import LineBotApi

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
            self.__data=info["permission2"]
            self.loaded+=1
        if mode&2 and not(self.loaded&2):
            #リクエストの読み込み
            self.__req=info["req_permit2"]
            self.loaded+=2
        return

    #読み込み
    #管理者追加リクエスト
    def Apply(self,userID,Name):
        add_data={userID:Name}
        self.__req.update(add_data)
        return "Success"
    #許可リクエスト
    def Allow(self,userID):
        print(self.__req)
        if userID in self.__req:
            print(self.__req)
            self.__data.update({userID:self.__req[userID]})
            self.__req.pop(userID)
            return "Success"
        else:
            return "Not Found the user"
    #削除
    def Del(self,userID):
        if userID in self.__data:
            self.__data.pop(userID)
            return "Success"
        else:
            return "Not Found the user"
    #管理者ログインチェック
    def Check(self,userID):
        if userID=="":
            return False
        if self.__data.get(userID):
            return True
        return False
    #管理者リスト
    def User_lists(self):
        return [self.__data,self.__req]
