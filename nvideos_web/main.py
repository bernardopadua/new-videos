# FLASK
from flask import Flask, url_for, session

# NVIDEOS
from user_details.view import ud

# CONFIG
from config import load_dotenv

from typing import Protocol
from dataclasses import dataclass

app = Flask(__name__)
app.config.from_file(".env", load_dotenv)

@dataclass
class IB:
    id:int 
    name: str

@dataclass
class IBB:
    idd:int 
    name: str


class Ab(Protocol):
    def test(self):
        pass

@dataclass(frozen=True)
class imutObj:
    real: int

class Abc(Ab):
    def __init__(self, id:int) -> None:
        super().__init__()
        self.nid = id
        self.idd: imutObj = imutObj(id)
        self._al = []

    # def __hash__(self) -> int:
    #     #return hash(self.idd.real)
    #     return hash(self.nid)

    # def __eq__(self, value: object) -> bool:
    #     if self.__class__ == value.__class__:
    #         return self.nid == value.nid
    #     if type(value) == int:
    #         return self.nid == value
    #     return (
    #         self.__class__ == value.__class__ and
    #         #self.idd.real == value.idd.real
    #         self.nid == value.nid
    #    )

    def ooo(self, t: IB):
        self._al.append(t)
    
    def oo(self, t: IB):
        return t in self._al

a = IB(id=1, name="abc")
y = IB(id=2, name="abc")
b = IBB(idd=1, name="abc2")

c = Abc(1)
d = Abc(1)

ii = set()
ii.add(c)
ii.add(1)

# ii = {}
# ii[c] = 123

def aab(number):
    print(number)

c.ooo(a)
c.ooo(b)

app.register_blueprint(ud)




@app.route("/abc/")
def abc():
    session["user"] = {"a": 22}
    return "Hello"

@app.route("/")
def index():
    return f"""
        <h1>Index</h1>
        <a href='{url_for("abc")}'>
            Abc
        </a>
        <br>
        <a href='{url_for("user_details.userIndex")}'>
            User Det
        </a>
    """

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, True, False)