# FLASK
from flask import session, redirect, url_for
from werkzeug.wrappers import Response

# BUILT-IN
from functools import wraps

# SERVICES
from nvideos_web.services.channel.service import ChannelService, Channel

# TYPING
from typing import Callable, Any
from collections.abc import Sequence, Mapping

def loginRequired(f: Callable[..., Any]) -> Callable[..., Response]:
    @wraps(f)
    def decorated_function(*args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Response:
        if not session.get("userId"):
            return redirect(url_for("home.login"))
        return f(*args, **kwargs)
    return decorated_function

def channelRequired(f: Callable[..., Any]) -> Callable[..., Response]:
    @wraps(f)
    def decorated_function(*args: Sequence[Any], **kwargs: Mapping[str, Any]) -> Response:
        if not session.get("channelId"):
            chSrv: ChannelService = ChannelService(userId=session.get("userId"))
            channel: Channel | None = chSrv.doIAlreadyHaveChannel()
            if channel:
                session["channelId"] = channel.channelId

        if not session.get("channelId"):
            return redirect(url_for("channel.create_channel"))

        return f(*args, **kwargs)
    return decorated_function
