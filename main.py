from flask import Flask, url_for
from user_details.view import ud

app = Flask(__name__)

app.register_blueprint(ud)

@app.route("/abc/")
def abc():
    return "abc"

@app.route("/")
def index():
    return f"""
        <h1>Index</h1>
        <a href='{url_for("user_details.userIndex")}'>
            User Det
        </a>
    """

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, True, False)