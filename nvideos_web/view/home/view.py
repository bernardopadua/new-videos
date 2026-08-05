# FLASK
from flask import (
    url_for, 
    Blueprint, 
    make_response, 
    render_template,
    request as flaskRequest
)

# SERVICE
from nvideos_web.services.user.service import UserService

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

        except Exception:
            #TODO: Add logger to log information of the exception
            return render_template("base/error.html")
        
        return "POST"

    templateRender = render_template("home/register_user.html")
    return templateRender

@homeBp.route("/player")
def index_player():
    urlPlayer = url_for("home.static", filename="player.js")
    page_resp = f"""
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
        </head>
        <h1>11</h1>
        <video id="video" controls style="width: 100%; max-width: 640px;"></video>
        <script src='{urlPlayer}'></script>
        </html>
    """
    resp = make_response(page_resp)

    cspPol = "script-src 'self' https://cdn.jsdelivr.net;"
    cspPol = f"{cspPol}connect-src 'self' http://localhost:8099;"

    resp.headers['Content-Security-Policy'] = cspPol
    return resp

@homeBp.route("/abc/<int:seconds>")
def abc(seconds: int = 0):
    from nvideos_web.services.user.service import UserService
    from nvideos_web.services.channel.service import ChannelService
    from nvideos_web.services.subscriber.service import SubscriberService

    # cc = ChannelService()
    # _ = cc.fillInputData(channelName="New Channel 2")

    us = UserService()
    user = us.selectByUserName("User1")

    user = us.fillInputData(
        userName="New Test2",
        userEmail="newtest2@test.com.br",
        userSurname="Test2",
        userPassword="123456",
        userIsActive=True,
        createSystemUser=True
    ).createNewUser()
    print(user)

    # us = UserService(userId=9)
    # user = us.fillInputData(userName="Changing name 1").updateUserById(44)
    # user = us.deleteByUserId(10)
    #print(user)
    
    # ch = ChannelService(userId=10)
    # ch.checkIdExists(10)
    # ch.fillInputData(
    #     channelName="Testing channel 1"
    # ).createNewChannel()

    sub = SubscriberService(userId=3).subscribeToChannel(channelId=3)

    return "<h1>Hello</h1>"