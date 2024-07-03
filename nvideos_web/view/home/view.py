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
    from nvideos_web.services.user.service import UserService

    u = UserService()
    nInput = u.setUserInput(
        userName="sdf",
        userEmail="dsafsdf",
        userSurname="sdfsdf",
        userPassword="sdfsdfsdfs",
        createSystemUser=True
    ).getUserInput()
    u.createNewUser()
    return "<h1>Hello</h1>"