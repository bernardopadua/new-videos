# FLASK
from flask import url_for, Blueprint

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

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

@homeBp.route("/abc/<int:seconds>")
def abc(seconds: int = 0):
    import threading, time
    from nvideos_web.services.user.user_service import UserService

    u = UserService()
    nInput = u.setUserInput(
        userName="sdf",
        userEmail="dsafsdf",
        userSurname="sdfsdf",
        userPassword="sdfsdfsdfs",
        createSystemUser=True
    )
    u.createNewUser()

    ini = time.perf_counter()
    viewResult = u.perfShow(0)
    time.sleep(seconds)
    end = time.perf_counter() - ini

    script = """
        setTimeout(()=>{
            location.reload()
        });
    """
    script = None

    return f"""
        <h1>Abc</h1>
            Thread::{threading.get_ident()}<br>
            Time::{end}<br>
        <br>

        {viewResult}

        <br>
        <a href='{url_for("home.index")}'>
            Index
        </a>
        <script>
            {script}
        </script>
    """