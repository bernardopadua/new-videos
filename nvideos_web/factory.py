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
from nvideos_web.view.subscriber.view import subscriberBp

# GLOBALS
from nvideos_web.view.template_context import register_globals_app

nvideosApp: Flask

def createApp() -> Flask:
    NewVideosDBContext.initDBContext()
    nvideosApp = Flask(__name__)
    _ = nvideosApp.config.from_file(".env.flask", loadDotEnv)

    register_globals_app(nvideosApp)

    nvideosApp.register_blueprint(baseBp)
    nvideosApp.register_blueprint(homeBp)
    nvideosApp.register_blueprint(userDetailsBp)
    nvideosApp.register_blueprint(videoDetailsBp)
    nvideosApp.register_blueprint(channelDetailsBp)
    nvideosApp.register_blueprint(subscriberBp)

    return nvideosApp
