# FLASK
from flask import Flask, url_for, session

# DATABASE
from nvideos_web.db.context import NewVideosDBContext

# NVIDEOS
from nvideos_web.user_details.view import ud

# CONFIG
from nvideos_web.config import load_dotenv

NewVideosDBContext.initPool()
app = Flask(__name__)
app.config.from_file(".env.flask", load_dotenv)

app.register_blueprint(ud)

@app.route("/abc/")
def abc():
    import threading, time

    ini = time.monotonic()
    tconn = None

    results = []
    with NewVideosDBContext.getConn() as conn:
        cur = conn.cursor()
        tconn = conn.__repr__

        cur.execute("SELECT * FROM nvideos_user;")
        results = cur.fetchall()

    end = time.monotonic() - ini

    script = """
        setTimeout(()=>{
            location.reload()
        });
    """
    #script = None

    return f"""
        <h1>Abc</h1>
            Thread::{threading.get_ident()}<br>
            Time::{end}<br>
            Conn::{tconn}
        <br>
            {results}
        <br>

        <a href='{url_for("index")}'>
            Index
        </a>
        <script>
            {script}
        </script>
    """

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