# FLASK
from flask import (
    Blueprint, redirect, render_template, request as flaskRequest, 
    session, url_for
)

# DECORATORS
from nvideos_web.view.endpoint_decorators import loginRequired

# SERVICE
from nvideos_web.services.channel.service import ChannelService, Channel

channelDetailsBp = Blueprint(
    "channel_details", __name__,
    static_folder="static", static_url_path="/channel_details/static",
    template_folder="template"
)

@channelDetailsBp.route("/channel/<int:channel_id>")
def channel_detail(channel_id):
    renderTemplate = render_template("channel/channel_detail.html", channel_id=channel_id)
    return renderTemplate

@channelDetailsBp.route("/channel/create", methods=["GET", "POST"])
@loginRequired
def channel_create():
    if flaskRequest.method == "POST":
        formData:dict[str,str] = flaskRequest.form
        cSrv: ChannelService = ChannelService(userId=session.get("userId"))

        try:
            channelCreated: Channel = cSrv.fillInputData(
                channelName=formData.get("channelName"),
                channelDescription=formData.get("channelDescription"),
                
            ).checkInputDataIsValid().createNewChannel()

            channelCreated = cSrv.moveTempImagesToMedia(
                channelId=channelCreated.channelId,
                avatarTempName=\
                    formData.get("avatarFileNameMediaServer") \
                    if formData.get("avatarFileNameMediaServer") != channelCreated.channelAvatarUrl \
                    else None,
                coverTempName=\
                    formData.get("bannerCoverImageUrl") \
                    if formData.get("bannerCoverImageUrl") != channelCreated.channelImageUrl \
                    else None
            ).fillInputData().updateChannelById(channelCreated.channelId)

            return redirect(url_for("channel/channel_details.channel_detail", channel_id=channelCreated.channelId))
        except Exception as e:
            return render_template("base/error.html", error=str(e))
    
    try:
        cSrv: ChannelService = ChannelService(userId=session.get("userId"))
        channel: Channel | None = cSrv.doIAlreadyHaveChannel()
        if channel:
            return redirect(url_for("channel_details.channel_detail", channel_id=channel.channelId))
    except:
        return render_template("base/error.html")

    return render_template("channel/channel_details_edit.html")

@channelDetailsBp.route("/channel/<int:channel_id>/edit", methods=["GET", "POST"])
@loginRequired
def channel_edit(channel_id):
    cSrv: ChannelService = ChannelService(userId=session.get("userId"))
    channel: Channel | None = cSrv.doIAlreadyHaveChannel()
    
    if channel is None:
        return render_template("base/error.html", error="You cant edit a channel that doesn't exists.")

    if flaskRequest.method == "POST":
        formData:dict[str,str] = flaskRequest.form
        try:
            channelUpdated: Channel = cSrv.fillInputData(
                channelName=formData.get("channelName"),
                channelDescription=formData.get("channelDescription")                
            #TODO: admin edit will use this same endpoint.
            ).checkInputDataIsValid().updateChannelById(channel.channelId) 

            channelUpdated = cSrv.moveTempImagesToMedia(
                channelId=channelUpdated.channelId,
                avatarTempName=\
                    formData.get("avatarFileNameMediaServer") \
                    if formData.get("avatarFileNameMediaServer") != channel.channelAvatarUrl \
                    else None,
                coverTempName=\
                    formData.get("bannerCoverImageUrl") \
                    if formData.get("bannerCoverImageUrl") != channelUpdated.channelImageUrl \
                    else None
            ).fillInputData().updateChannelById(channelUpdated.channelId)

            return redirect(url_for("channel/channel_details.channel_detail", channel_id=channelUpdated.channelId))
        except Exception as e:
            return render_template("base/error.html", error=str(e))

    try:
        return render_template("channel/channel_details_edit.html", ch=channel)
    except Exception as e:
        return render_template("base/error.html")
