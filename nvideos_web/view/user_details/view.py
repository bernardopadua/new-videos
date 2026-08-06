# FLASK
from flask import (
    Blueprint, session, render_template, 
    request as flaskRequest
)

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
        userId: int = session["userId"]
        uSrv: UserService = UserService(userId=userId)
        passwordOption: dict[str, Any] = {}

        if flaskRequest.form.get("userPassword") != "": 
            passwordOption = {
                "userPassword": flaskRequest.form.get("userPassword"),
                "confirmPassword": flaskRequest.form.get("confirmPassword")
            }

        try:
            userUpdated = uSrv.fillInputData(
                userName=flaskRequest.form.get("userName"),
                userSurname=flaskRequest.form.get("userSurname"),
                userEmail=flaskRequest.form.get("userEmail"),
                userBirthDate=uSrv.getDatetimeFromDate(flaskRequest.form.get("birthDate")),
                **passwordOption
            ).checkInputDataIsValid().updateUserById(session["userId"])

            if flaskRequest.form.get("avatarFileNameMediaServer") != \
                userUpdated.userAvatarUrl:
                userUpdated = uSrv.moveTempAvatarToMedia(
                    userId, 
                    flaskRequest.form.get("avatarFileNameMediaServer")
                ).fillInputData().updateUserById(
                    userId,
                    updatedByUserId=userId
                )
            
            uSrv.fillUserSession(userUpdated)
        except Exception as e:
            return render_template("base/error.html", error=str(e))

        return render_template(
            "user_details_edit.html",
            us=userUpdated,
            success=True
        )

    us: User = UserService(userId=session["userId"]).selectByUserId()
    return render_template(
        "user_details_edit.html",
        us=us
    )
