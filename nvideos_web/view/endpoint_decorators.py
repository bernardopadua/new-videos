# FLASK
from flask import session, redirect, url_for
from werkzeug.wrappers import Response

# BUILT-IN
from functools import wraps

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
