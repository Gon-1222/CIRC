import json
import os
from File import Gfile

class notify(Gfile):
    data=[]
    #ロード（コンストラクタ）
    def __init__(self):
        self.data=self.load_file("1nS6ug9PSR5QNN8iWism-oRn-HZvyQPL-")
        return
    #セーブ
    def save(self):
        self.Clean_Up()
        self.save_file("1nS6ug9PSR5QNN8iWism-oRn-HZvyQPL-",self.data)
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
