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

def getChannelNameAbreviation(name: str) -> str:
    import re
    newName = "".join(re.findall(r"[A-Z]", name))
    if len(newName) < 2:
        newName = name[:2]
    elif len(newName) > 2:
        newName = newName[:2]
    
    return newName

def getChannelSubscriberDescription(totalSubscribers: int) -> str:
    if totalSubscribers > 1000 and totalSubscribers < 1000000:
        total = str(totalSubscribers/1000)
        if total.find(".") == -1:
            return total + "K"
        else:
            return total[:total.find(".")] + "K"
    elif totalSubscribers > 1000000:
        total = str(totalSubscribers/1000000)
        if total.find(".") == -1:
            return total + "M"
        else:
            return total[:total.find(".")] + "M"
    else:
        return str(totalSubscribers)

#Don't know if it is the best solution.
def register_globals_app(app: Flask):
    cast(dict[str, Any], app.jinja_env.globals)["userIsLoggedIn"] = userIsLoggedIn
    cast(dict[str, Any], app.jinja_env.globals)["getUserAvatar"] = getUserAvatar
    cast(dict[str, Any], app.jinja_env.globals)["getDateToinput"] = getDateToinput
    cast(dict[str, Any], app.jinja_env.globals)["getVideoPermissionTranslated"] = getVideoPermissionTranslated
    cast(dict[str, Any], app.jinja_env.globals)["getChannelNameAbreviation"] = getChannelNameAbreviation
    cast(dict[str, Any], app.jinja_env.globals)["getChannelSubscriberDescription"] = getChannelSubscriberDescription