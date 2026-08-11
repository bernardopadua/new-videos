# FLASK
from flask import Flask, session

# BUILT-IN
from datetime import date

# TYPING
from typing import cast, Any

# SERVICES
from nvideos_web.services.video.service import VideoService

def userIsLoggedIn() -> bool:
    return session.get("userId") is not None

def getUserAvatar() -> str | None:
    return session.get("userAvatarUrl")

def getDateToinput(dateTime: date) -> str:
    return dateTime.strftime("%Y-%m-%d")

def getVideoPermissionTranslated(permission: str) -> str:
    vSrv = VideoService()
    return vSrv.translateHtmlVideoPermission(permission)

#Don't know if it is the best solution.
def register_globals_app(app: Flask):
    cast(dict[str, Any], app.jinja_env.globals)["userIsLoggedIn"] = userIsLoggedIn
    cast(dict[str, Any], app.jinja_env.globals)["getUserAvatar"] = getUserAvatar
    cast(dict[str, Any], app.jinja_env.globals)["getDateToinput"] = getDateToinput
    cast(dict[str, Any], app.jinja_env.globals)["getVideoPermissionTranslated"] = getVideoPermissionTranslated