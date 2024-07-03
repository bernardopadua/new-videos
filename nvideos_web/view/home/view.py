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

    # us = UserService()
    # nInput = us.fillInputData(
    #     userName="sdf",
    #     userEmail="dsafsdf",
    #     userSurname="sdfsdf",
    #     userPassword="sdfsdfsdfs",
    #     createSystemUser=True
    # ).getInputData()
    # us.createNewUser()
    us = UserService(userId=9)
    us.fillInputData(userName="Changing name 1").updateUserById(10)
    return "<h1>Hello</h1>"