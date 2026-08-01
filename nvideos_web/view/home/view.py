# FLASK
from flask import url_for, Blueprint, make_response, render_template

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

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

@homeBp.route("/registration")
def user_registration():
    templateRender = render_template("home/register_user.html")

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

@homeBp.route("/home")
def home():
    return f"""
        <h1>Index</h1>
        <a href='{url_for("home.abc")}'>
            Abc
        </a>
        <br>
        <a href='{url_for("user_details.userIndex")}'>
            User Det
        </a>
    """

@homeBp.route("/abc/<int:seconds>")
def abc(seconds: int = 0):
    from nvideos_web.services.user.service import UserService
    from nvideos_web.services.channel.service import ChannelService
    from nvideos_web.services.subscriber.service import SubscriberService

    # us = UserService()
    # user = us.fillInputData(
    #     userName="New Test",
    #     userEmail="newtest@test.com.br",
    #     userSurname="Test",
    #     userPassword="123456",
    #     userIsActive=True,
    #     createSystemUser=True
    # ).createNewUser()
    # print(user)

    # us = UserService(userId=9)
    # user = us.fillInputData(userName="Changing name 1").updateUserById(44)
    # user = us.deleteByUserId(10)
    #print(user)
    
    # ch = ChannelService(userId=10)
    # ch.checkIdExists(10)
    # ch.fillInputData(
    #     channelName="Testing channel 1"
    # ).createNewChannel()

    sub = SubscriberService(userId=49).subscribeToChannel(channelId=4)

    return "<h1>Hello</h1>"