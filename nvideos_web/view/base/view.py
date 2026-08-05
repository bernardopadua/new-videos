# FLASK
from flask import Blueprint

baseBp = Blueprint(
    "base", __name__, 
    static_folder="static",
    static_url_path="/base/static/",
    template_folder="template"
)