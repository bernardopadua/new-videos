# FLASK
from flask import (
    Blueprint, render_template, 
    request as flaskRequest, redirect, session
)

# DB 
from nvideos_web.db.redis import nredis

# SERVICE
from nvideos_web.services.base.error import ServiceException
from nvideos_web.services.subscriber.service import SubscriberService
from nvideos_web.services.user.service import UserService
from nvideos_web.services.channel.service import ChannelService

# ERRORs
from nvideos_web.services.user.error import UserServiceUserHasInvalidEmail

# DECORATORS
from nvideos_web.view.endpoint_decorators import loginRequired

homeBp = Blueprint(
    "home", __name__, 
    static_folder='static', 
    static_url_path="/home/static",
    template_folder="template"
)

@homeBp.route("/")
def index_home():
    templateRender = render_template("home/home.html")
    return templateRender

@homeBp.route("/login", methods=["GET", "POST"])
def login():
    if flaskRequest.method == "POST":
        userEmail = flaskRequest.form.get("userEmail")
        userPassword = flaskRequest.form.get("userPassword")
    
        if not userEmail or not userPassword:
            return render_template("home/login.html", error="Email and password are required.")
        
        try:
            uSrv = UserService()
            if (usu := uSrv.userLogin(userEmail, userPassword)) is None:
                return render_template("home/login.html", error="Email or password incorrect.")

            ch = ChannelService(userId=usu.userId)
            channel = ch.doIAlreadyHaveChannel()

            if channel:
                uSrv.setUserChannel(channel.channelId)

            ss = SubscriberService(userId=usu.userId)
            chs = ss.selectChannelsUserIsSubscribed()

            if chs is not None:
                from nvideos_web.db.redis_constants import USER_SUBSCRIBED_CHANNELS_KEY
                import json
                _ = nredis.client.set(
                    USER_SUBSCRIBED_CHANNELS_KEY.format(userId=usu.userId),
                    json.dumps(chs)
                )
            
            if (nextPath := session.pop("next", None)) is not None:
                return redirect(nextPath)

            return redirect("/")                
        except ServiceException as e:
            return render_template("base/error.html", error=str(e))
        except Exception as e:
            return render_template("base/error.html")
            
    templateRender = render_template("home/login.html")
    return templateRender

@homeBp.route("/logout")
@loginRequired
def logout():
    from flask import session, redirect
    session.clear()
    return redirect("/")

@homeBp.route("/register", methods=["GET", "POST"])
def user_registration():
    if flaskRequest.method == "POST":
        try:
            #Create then update, for now I will maintain this way, but for large scale 
            #one session with insert would be the best.

            uSrv = UserService()
            
            userCreated = uSrv.setUserPermission(
                normalUser=True
            ).fillInputData(
                userName=flaskRequest.form.get("userName"),
                userSurname=flaskRequest.form.get("userSurname"),
                userEmail=flaskRequest.form.get("userEmail"),
                userBirthDate=uSrv.getDatetimeFromDate(flaskRequest.form.get("birthDate")),
                userPassword=flaskRequest.form.get("userPassword"),
                confirmPassword=flaskRequest.form.get("confirmPassword"),
                userIsActive=True
            ).checkInputDataIsValid().createNewUser()
            
            if flaskRequest.form.get("avatarFileNameMediaServer") != "":
                userCreated = uSrv.moveTempAvatarToMedia(
                    userCreated.userId, 
                    flaskRequest.form.get("avatarFileNameMediaServer")
                ).fillInputData().updateUserById(
                    userCreated.userId,
                    updatedByUserId=userCreated.userId
                )

            templateRender = render_template("home/user_registration_success.html", userName=userCreated.userName)
            return templateRender

        except UserServiceUserHasInvalidEmail as e:
            return render_template("base/error.html", error=str(e))
        except Exception:
            #TODO: Add logger to log information of the exception
            return render_template("base/error.html")

    templateRender = render_template("home/register_user.html")
    return templateRender
