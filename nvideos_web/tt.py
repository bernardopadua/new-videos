from dataclasses import dataclass

@dataclass
class Abcd:
    id: int
    name: str

class Abc(Abcd):
    def __init__(self, pname:str):
        self.name = pname

aa = Abc("pimptech")

print(aa.name)