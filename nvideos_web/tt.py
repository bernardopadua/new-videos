from dataclasses import dataclass
from nvideos_web.db.context import DatabaseContext

@dataclass
class Abcd:
    id: int
    name: str

class Abc(Abcd):
    def __init__(self, pname:str):
        self.name = pname

aa = Abc("pimptech")
print(aa.name)

DatabaseContext.initConn()
DatabaseContext.getConn()
