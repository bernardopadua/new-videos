# FLASK
from flask import Flask, session

# BUILT-IN
from datetime import date

# TYPING
from typing import cast, Any

def userIsLoggedIn() -> bool:
    return session.get("userId") is not None

def getUserAvatar() -> str | None:
    return session.get("userAvatarUrl")

def getDateToinput(dateTime: date) -> str:
    return dateTime.strftime("%Y-%m-%d")

#Don't know if it is the best solution.
def register_globals_app(app: Flask):
    cast(dict[str, Any], app.jinja_env.globals)["userIsLoggedIn"] = userIsLoggedIn
    cast(dict[str, Any], app.jinja_env.globals)["getUserAvatar"] = getUserAvatar
    cast(dict[str, Any], app.jinja_env.globals)["getDateToinput"] = getDateToinput