# FLASK
from flask import Flask, url_for, session

# NVIDEOS
from user_details.view import ud

# CONFIG
from config import load_dotenv

from abc import abstractmethod
from typing import Protocol
from dataclasses import dataclass

app = Flask(__name__)
app.config.from_file(".env", load_dotenv)

app.register_blueprint(ud)


class Ur(Protocol):
    @abstractmethod
    def add_user(self, name: str) -> None:
        raise NotImplemented

    @abstractmethod
    def get_id(self, username: int) -> int:
        raise NotImplemented

class UserR(Ur):
    def __init__(self) -> None:
        self._countId = 0

        self.users = {}

    def add_user(self, name:str):
        self._countId += 1
        self.users[name] = self._countId

def addUser(user: Ur, name: str):
    user.add_user(name)

a = UserR()
addUser(a, "pimptech")

exit()

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