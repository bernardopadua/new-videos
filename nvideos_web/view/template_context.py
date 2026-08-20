# FLASK
from flask import Flask, session, current_app as app

# BUILT-IN
from datetime import date, datetime

# TYPING
from typing import cast, Any

# DB
from nvideos_web.db.redis import nredis

# SERVICES
from nvideos_web.services.video.service import VideoService
from nvideos_web.services.channel.service import ChannelService

def userIsLoggedIn() -> bool:
    return session.get("userId") is not None

def getCurrentUserId() -> int | None:
    currentUser = cast(int | None, session.get("userId", None)) #pywright
    return currentUser

def getUserAvatar() -> str | None:
    user = cast(dict[str, object] | None, session.get("user"))
    if user:
        avatar = user.get("userAvatarUrl")
        if avatar is not None:
            return cast(str, avatar)
    return None

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

def getTotalViewsDescription(totalViews: int) -> str:
    if totalViews > 1000 and totalViews < 1000000:
        total = str(totalViews/1000)
        if total.find(".") == -1:
            return total + "K views"
        else:
            return total[:total.find(".")] + "K views"
    elif totalViews > 1000000:
        total = str(totalViews/1000000)
        if total.find(".") == -1:
            return total + "M views"
        else:
            return total[:total.find(".")] + "M views"
    else:
        return str(totalViews) + " views"

def formatTimeVideoDuration(timeDurationSeconds: int):
    hours: str = str(round(timeDurationSeconds / 3600)).zfill(2) if timeDurationSeconds > 3600 else "00"
    minutes: str = str(round((timeDurationSeconds % 3600) / 60)).zfill(2)
    seconds: str = str(round(timeDurationSeconds % 60)).zfill(2)

    if hours == "00":
        return minutes + ":" + seconds
    return hours + ":" + minutes + ":" + seconds

def formatDatetimeToString(dateTime: str) -> str:
    dt = datetime.fromisoformat(dateTime)
    return datetime.strftime(dt, "%Y-%m-%d %H:%M:%S")

def getChannelsSubscribers() -> list[dict[str, str]] | None:
    import json
    from nvideos_web.db.redis_constants import USER_SUBSCRIBED_CHANNELS_KEY

    r = nredis.client
    userId = session.get("userId")

    if userId is None:
        return None

    result = r.get(
        USER_SUBSCRIBED_CHANNELS_KEY.format(userId=userId)
    )

    if not result:
        return None
    if not isinstance(result, (str,bytes)):
        return None

    return json.loads(result)

def userHasChannel() -> bool:
    """
    Checks if the user has a channel.
    """
    if not userIsLoggedIn():
        return False

    if ChannelService(userId=session.get("userId")).doIAlreadyHaveChannel() is None:
        return False
    
    return True

#Don't know if it is the best solution.
def register_globals_app(app: Flask):
    cast(dict[str, Any], app.jinja_env.globals)["userIsLoggedIn"] = userIsLoggedIn
    cast(dict[str, Any], app.jinja_env.globals)["getUserAvatar"] = getUserAvatar
    cast(dict[str, Any], app.jinja_env.globals)["getDateToinput"] = getDateToinput
    cast(dict[str, Any], app.jinja_env.globals)["getVideoPermissionTranslated"] = getVideoPermissionTranslated
    cast(dict[str, Any], app.jinja_env.globals)["getChannelNameAbreviation"] = getChannelNameAbreviation
    cast(dict[str, Any], app.jinja_env.globals)["getChannelSubscriberDescription"] = getChannelSubscriberDescription
    cast(dict[str, Any], app.jinja_env.globals)["getTotalViewsDescription"] = getTotalViewsDescription
    cast(dict[str, Any], app.jinja_env.globals)["formatTimeVideoDuration"] = formatTimeVideoDuration
    cast(dict[str, Any], app.jinja_env.globals)["getChannelsSubscribers"] = getChannelsSubscribers
    cast(dict[str, Any], app.jinja_env.globals)["userHasChannel"] = userHasChannel
    cast(dict[str, Any], app.jinja_env.globals)["getCurrentUserId"] = getCurrentUserId
    cast(dict[str, Any], app.jinja_env.globals)["formatDatetimeToString"] = formatDatetimeToString
