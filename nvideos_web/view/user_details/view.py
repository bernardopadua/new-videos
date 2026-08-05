# FLASK
from flask import Blueprint, session, render_template, request as flaskRequest, jsonify
import flask

# SERVICE
from nvideos_web.services.user.service import UserService
from nvideos_web.core.entity.user import User

userDetailsBp = Blueprint(
    "user_details", __name__,
    static_folder="static", static_url_path="/user_details/static",
    template_folder="template"
)

@userDetailsBp.route("/profile", methods=["GET", "POST"])
def user_edit():
    if flaskRequest.method == "POST":
        uSrv: UserService = UserService(userId=session["userId"])

        _ = uSrv.fillInputData(
            userName=flaskRequest.form.get("userName"),
            userSurname=flaskRequest.form.get("userSurname"),
            userEmail=flaskRequest.form.get("userEmail"),
            userBirthDate=uSrv.getDatetimeFromDate(flaskRequest.form.get("birthDate")),
            userPassword=flaskRequest.form.get("userPassword"),
            confirmPassword=flaskRequest.form.get("confirmPassword"),
            #avatarUrl=flaskRequest.form.get("avatarFileNameMediaServer")
        ).checkInputDataIsValid().updateUserById(session["userId"])

    us: User = UserService(userId=session["userId"]).selectByUserId()
    return render_template(
        "user_details_edit.html",
        us=us
    )
