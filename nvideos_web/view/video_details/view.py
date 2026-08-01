# FLASK
from flask import Blueprint, render_template

videoDetailsBp = Blueprint(
    "video_details", __name__,
    static_folder="static", static_url_path="/video_details/static",
    template_folder="template"
)

@videoDetailsBp.route("/video/<video_key>")
def video_detail(video_key):
    renderTemplate = render_template("video_detail.html", video_key=video_key)
    return renderTemplate