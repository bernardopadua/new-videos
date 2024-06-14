from flask import Blueprint

ud = Blueprint("user_details", "user_details")

@ud.route("/user/")
def userIndex():
    return "userDetails"