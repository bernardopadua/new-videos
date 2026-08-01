# FLASK
from flask import Blueprint, session, render_template

userDetailsBp = Blueprint("user_details", __name__)

@userDetailsBp.route("/user/")
def user_index():
    if not "user" in session:
        return "No user"
    else:
        u = session["user"]
        return f"user: "
    return "userDetails"