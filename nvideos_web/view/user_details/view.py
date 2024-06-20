from flask import Blueprint, session

ud = Blueprint("user_details", "user_details")

@ud.route("/user/")
def userIndex():
    if not "user" in session:
        return "No user"
    else:
        u = session["user"]
        return f"user: "
    return "userDetails"