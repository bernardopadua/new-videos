# FLASK
from flask import Flask, url_for, session

# NVIDEOS
from user_details.view import ud

# CONFIG
from config import load_dotenv

app = Flask(__name__)
app.config.from_file(".env", load_dotenv)

class Abc:
    def __init__(self) -> None:
        self.id = 1

app.register_blueprint(ud)

@app.route("/abc/")
def abc():
    ab = Abc()
    session["user"] = ab
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