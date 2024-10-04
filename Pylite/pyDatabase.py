import json
from typing import Optional

from Pylite.pyColumn import Column
from .pyTable import Table
from .pyTools import *

class Database():
    def __init__(self,path="",key=""):
        self.path = path
        self.key = key
        self.Tables = {}
        if path != "":
            try:
                with open(path,"r",encoding="UTF16") as f:
                    data = json.loads(Decrypt(f.read(),self.key))
                    for k,v in data["Tables"].items():
                        t = self.CreateTable(k)
                        for c in v["Columns"].keys():
                            t.Columns[c] = Column(v["Columns"][c]["Type"],v["Columns"][c]["Options"])
                            t.Columns[c].Data = v["Columns"][c]["Data"]
            except FileNotFoundError:
                raise FileNotFoundError(f"File '{path}' not found.")
            except json.JSONDecodeError:
                raise Exception("Incorrect Password")
        
    
    def __getattr__(self, name: str) -> Optional[Table]:
        if name in self.Tables:
            return self.Tables[name]
        raise AttributeError(f"Table '{name}' not found.")
    
    def CreateTable(self,TableName) -> Table:
        self.Tables[TableName] = Table(TableName)
        self.add_property(TableName)
        return self.Tables[TableName]
    
    def RenameTable(self,OldName,NewName):
        self.Tables[NewName] = self.Tables.pop(OldName)
        self.Tables[NewName].TableName = NewName
        setattr(self.__class__, NewName, property(lambda self, name=NewName: self.Tables[name]))
        delattr(self.__class__, OldName)
    
    def DeleteTable(self,TableName):
        del self.Tables[TableName]
        delattr(self.__class__, TableName)
    
    def __len__(self) -> int:
        return len(self.Tables.keys())
    
    def add_property(self, name):
        setattr(self.__class__, name, property(lambda self: self.Tables[name]))
    
    def Save(self,Path):
        file = json.dumps({
            "Tables": {k:{
                "Columns":{c:{
                    "Type":v.Columns[c].Type.__name__,
                    "Data":v.Columns[c].Data,
                    "Options":v.Columns[c].Options
                    } for c in v.Columns.keys()}
                } for k,v in self.Tables.items()}
        })
        with open(Path,"w",encoding="UTF16") as f:
            f.write(Crypt(file,self.key))
        
    @staticmethod
    def Load(path):
        with open(path,"r") as f:
            data = json.loads(f.read())
            db = Database()
            for k,v in data["Tables"].items():
                t = db.CreateTable(k)
                for c in v["Columns"].keys():
                    t.Columns[c] = Column(v["Columns"][c]["Type"],v["Columns"][c]["Options"])
                    # t.AddColumn(c,eval(v["Columns"][c]["Type"]),v["Columns"][c]["Options"])
                    t.Columns[c].Data = v["Columns"][c]["Data"]
        return db
            
    