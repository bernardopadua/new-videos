# FLASK
from flask import Blueprint, session, render_template

ud = Blueprint("user_details", __name__)

@ud.route("/user/")
def user_index():
    if not "user" in session:
        return "No user"
    else:
        u = session["user"]
        return f"user: "
    return "userDetails"