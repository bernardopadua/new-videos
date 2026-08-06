# FLASK
from flask import Blueprint, render_template

channelDetailsBp = Blueprint(
    "channel_details", __name__,
    static_folder="static", static_url_path="/channel_details/static",
    template_folder="template"
)

@channelDetailsBp.route("/channel/<int:channel_id>")
def channel_detail(channel_id):
    renderTemplate = render_template("channel_detail.html", channel_id=channel_id)
    return renderTemplate

@channelDetailsBp.route("/channel/create")
def channel_create():
    return render_template("channel_details_edit.html")

@channelDetailsBp.route("/channel/<int:channel_id>/edit")
def channel_edit(channel_id):
    return render_template("channel_details_edit.html", channel_id=channel_id)