# FLASK
from flask import Blueprint, session, render_template, request as flaskRequest, jsonify

# SERVICE
from nvideos_web.services.user.service import UserService
from nvideos_web.core.entity.user import User

userDetailsBp = Blueprint(
    "user_details", __name__,
    static_folder="static", static_url_path="/user_details/static",
    template_folder="template"
)

@userDetailsBp.route("/profile")
def user_edit():
    us: User = UserService(userId=session["userId"]).selectByUserId()

    return render_template(
        "user_details_edit.html",
        user=us
    )
