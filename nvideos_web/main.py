# FLASK
from flask import Flask, url_for, session

# NVIDEOS
from user_details.view import ud

# CONFIG
from config import load_dotenv

from typing import Protocol

app = Flask(__name__)
app.config.from_file(".env", load_dotenv)

class Ab(Protocol):
    def test(self):
        pass

class Abc(Ab):
    def ooo(self):
        pass

ac = Abc()

app.register_blueprint(ud)

@app.route("/abc/")
def abc():
    ab = Abc()
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