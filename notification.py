import json
import os
import datetime
#from File import Gfile

class notify():
    data=[]
    #ロード（コンストラクタ）
    def __init__(self,info):
        self.data=info
        return
    #過去の日付を削除する
    def Clean_Up(self):
        current_dt=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
        #修正
        current_dt=current_dt.replace(hour=0,minute=0,second=0,microsecond=0)
        Flag=True
        while(Flag):
            Flag=False
            for i in self.data:
                buf = datetime.datetime.strptime(i,'%Y/%m/%d')
                buf = buf.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
                if buf<current_dt:
                    self.data.remove(i)
                    Flag=True
                    break

    #追加
    def Add(self,buf):
        self.data.append(buf)
