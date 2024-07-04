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
    # user = us.fillInputData(
    #     userName="New Test",
    #     userEmail="newtest@test.com.br",
    #     userSurname="Test",
    #     userPassword="123456",
    #     userIsActive=True,
    #     createSystemUser=True
    # ).createNewUser()
    # print(user)
    us = UserService(userId=9)
    user = us.fillInputData(userName="Changing name 1").updateUserById(44)
    # user = us.deleteByUserId(10)
    print(user)
    return "<h1>Hello</h1>"