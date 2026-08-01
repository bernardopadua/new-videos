# FLASK
from flask import Flask

# DATABASE
from nvideos_web.db.pgcontext import NewVideosDBContext

# CONFIG 
from nvideos_web.config import loadDotEnv

# VIEWS
from nvideos_web.view.base.view import baseTemplate
from nvideos_web.view.user_details.view import ud
from nvideos_web.view.home.view import homeBp

def createApp() -> Flask:
    NewVideosDBContext.initDBContext()
    app = Flask(__name__)
    app.config.from_file(".env.flask", loadDotEnv)

    app.register_blueprint(baseTemplate)
    app.register_blueprint(homeBp)
    app.register_blueprint(ud)

    return app
