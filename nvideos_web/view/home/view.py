# FLASK
from flask import url_for, Blueprint

# DB
from nvideos_web.db.context import NewVideosDBContext

homeBp = Blueprint("home", "home")

@homeBp.route("/")
def index():
    return f"""
        <h1>Index</h1>
        <a href='{url_for("home.abc")}'>
            Abc
        </a>
        <br>
        <a href='{url_for("user_details.userIndex")}'>
            User Det
        </a>
    """

@homeBp.route("/abc/")
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