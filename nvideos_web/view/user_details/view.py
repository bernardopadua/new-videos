# FLASK
from flask import Blueprint, session, render_template

userDetailsBp = Blueprint(
    "user_details", __name__,
    static_folder="static", static_url_path="/user_details/static",
    template_folder="template"
)

@userDetailsBp.route("/user/")
def user_index():
    if not "user" in session:
        return "No user"
    else:
        u = session["user"]
        return f"user: "
    return "userDetails"

@userDetailsBp.route("/user/edit")
def user_edit():
    return render_template("user_details_edit.html")