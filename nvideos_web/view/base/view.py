# FLASK
from flask import url_for, Blueprint

baseTemplate = Blueprint(
    "base", __name__, 
    static_folder="static",
    static_url_path="/base/static/",
    template_folder="template"
)