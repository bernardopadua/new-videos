from flask import Flask, session
from typing import cast, Any

def userIsLoggedIn() -> bool:
    return session.get("userId") is not None

def getUserAvatar() -> str | None:
    return session.get("userAvatarUrl")

#Don't know if it is the best solution.
def register_globals_app(app: Flask):
    cast(dict[str, Any], app.jinja_env.globals)["userIsLoggedIn"] = userIsLoggedIn
    cast(dict[str, Any], app.jinja_env.globals)["getUserAvatar"] = getUserAvatar