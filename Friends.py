import csv
class friend:
    member=[]
    #読み込み
    def __init__(self):
        with open("data/friends.dat","r") as f:
            reader = csv.reader(f)
            self.member=[i for i in reader]
    #書き込み
    def save(self):
        with open("data/friends.dat","w") as f:
            writer = csv.writer(f)
            writer.writerow(self.member)
    #追加
    def add(self,IDS):
        self.member.append(IDS)
    #削除
    def remove(self,IDS):
        self.member.remove(IDS)
    #リストを返す
    def LIST():
        return self.member
