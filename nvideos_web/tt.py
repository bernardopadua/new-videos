from dataclasses import dataclass
from nvideos_web.db.pgcontext import NewVideosDBContext

from typing import NewType

Permissions = NewType("Permissions", int)

perm: Permissions = 3

read_perm = 0b0001
write_perm = 0b0010
exec_perm = 0b0100
new_perm = 0b0100000000

print(perm)

@dataclass
class Abcd:
    id: int
    name: str

class Abc(Abcd):
    def __init__(self, pname:str):
        self.name = pname

# aa = Abc("pimptech")
# print(aa.name)

# NewVideosDBContext.initDBContext()
# NewVideosDBContext.getConn()
