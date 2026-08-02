# FLASK
from flask import Flask

# DATABASE
from nvideos_web.db.pgcontext import NewVideosDBContext

# CONFIG 
from nvideos_web.config import loadDotEnv

# VIEWS
from nvideos_web.view.base.view import baseBp
from nvideos_web.view.user_details.view import userDetailsBp
from nvideos_web.view.home.view import homeBp
from nvideos_web.view.video_details.view import videoDetailsBp
from nvideos_web.view.channel_details.view import channelDetailsBp

def createApp() -> Flask:
    NewVideosDBContext.initDBContext()
    app = Flask(__name__)
    app.config.from_file(".env.flask", loadDotEnv)

    app.register_blueprint(baseBp)
    app.register_blueprint(homeBp)
    app.register_blueprint(userDetailsBp)
    app.register_blueprint(videoDetailsBp)
    app.register_blueprint(channelDetailsBp)

    return app
