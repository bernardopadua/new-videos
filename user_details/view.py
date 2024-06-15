from flask import Blueprint
from models.user import User

ud = Blueprint("user_details", "user_details")

@ud.route("/user/")
def userIndex():
    
    return "userDetails"