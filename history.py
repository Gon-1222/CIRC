import json
import os
from File import Gfile

class History(Gfile):
        data=[]
        def Add(self,New_data):
            self.data=self.load_file("1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA")
            self.data.insert(0,New_data)
            self.save_file("1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA",self.data)
            return
        def Del(self,Del_data):
            self.data=self.load_file("1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA")
            if Del_data in self.data:
                self.data.remove(Del_data)
            self.save_file("1zsEmY3P-Ro_JzJWHi2xk5CFdzdixSKpA",self.data)
