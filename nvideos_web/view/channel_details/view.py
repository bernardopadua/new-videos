# FLASK
import json

from flask import (
    Blueprint, jsonify, redirect, render_template, request as flaskRequest, 
    session, url_for
)

# REDIS
from nvideos_web.db.redis import nredis
from nvideos_web.db.redis_constants import USER_SUBSCRIBED_CHANNELS_KEY

# DECORATORS
from nvideos_web.services.subscriber.service import SubscriberService
from nvideos_web.services.user.service import UserService
from nvideos_web.services.video.service import VideoService, VideoJson
from nvideos_web.view.endpoint_decorators import loginRequired, channelRequired

# TYPING
from typing import cast

# CONSTANTS
from nvideos_web.view.channel_details.constants import LIMIT_VIDEOS_CHANNEL

# ERROR
from nvideos_web.services.base.error import ServiceException

# SERVICE
from nvideos_web.services.subscriber.service import ChannelSubscribedList
from nvideos_web.services.channel.service import ChannelService

# ENTITY
from nvideos_web.core.entity.channel import Channel

channelDetailsBp = Blueprint(
    "channel_details", __name__,
    static_folder="static", static_url_path="/channel_details/static",
    template_folder="template"
)

@channelDetailsBp.route("/channel/my")
@channelRequired
@loginRequired
def channel_home():
    cSrv: ChannelService = ChannelService(userId=session.get("userId"))
    
    try:
        channel: Channel | None = cSrv.doIAlreadyHaveChannel()

        if channel is None:
            return redirect(url_for("channel_details.channel_create"))

        return render_template("channel/channel_detail.html", channel=channel)
    except ServiceException as e:
        return render_template("base/error.html", error=str(e))
    except Exception as e:
        #TODO: LOGGING
        return render_template("base/error.html")

@channelDetailsBp.route("/channel/<int:channel_id>")
@loginRequired
def channel_detail(channel_id: int):
    import json
    cs = ChannelService(userId=session.get("userId"))
    ss = SubscriberService(userId=session.get("userId"))

    try:
        channel = cs.selectChannelById(channel_id)
        if not channel:
            raise ServiceException("Channel does not exists.")

        vs = VideoService(userId=session.get("userId"), channelId=channel_id)

        userOwnChannel = cast(int, session.get("userId", 0)) == channel.userId

        channelsUserSubscribed = nredis.client.get(
            USER_SUBSCRIBED_CHANNELS_KEY.format(userId=session.get("userId"))
        )
        
        isSubscribed = False
        if channelsUserSubscribed:
            channelsUserSubscribed = json.loads(channelsUserSubscribed)
            isSubscribed = channel.channelId in channelsUserSubscribed

        totalSubscribers = ss.selectTotalSubscribers(channelId=channel_id)
        channelVideos, totalVideos = vs.selectLimitProcessedVideosByChannelId(
            limit=LIMIT_VIDEOS_CHANNEL,
            userOwnVideoChannel=userOwnChannel,
            userIsSubscribedToChannel=isSubscribed
        )
        lastVideo: VideoJson | None = None

        if channelVideos and len(channelVideos) > 0:
            lastVideo = channelVideos.pop(0)

        return render_template(
            "channel/channel_detail.html", 
            ch=channel, isSubscribed=isSubscribed,
            totalSubscribers=totalSubscribers,
            lastVideo=lastVideo,
            totalVideos=totalVideos, channelVideos=channelVideos,
            userOwnChannel=channel.userId == session.get("userId")
        )
    except ServiceException as e:
        return render_template("base/error.html", error=str(e))
    except Exception as e:

        #TODO: LOGGING
        return render_template("base/error.html")

@channelDetailsBp.route("/channel/create", methods=["GET", "POST"])
@loginRequired
def channel_create():
    if flaskRequest.method == "POST":
        formData:dict[str,str] = flaskRequest.form
        cSrv: ChannelService = ChannelService(userId=session.get("userId"))
        channelCreated: Channel | None = None

        try:
            channelCreated = cSrv.fillInputData(
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

            UserService().setUserChannel(channelCreated.channelId)

            return redirect(url_for("channel_details.channel_detail", channel_id=channelCreated.channelId))
        
        except ServiceException as e:
            if channelCreated:
                _ = cSrv.hardDeleteChannelById(channelCreated.channelId)

            return render_template("base/error.html", error=str(e))
        except Exception as e:
            #TODO: LOGGING.
            if channelCreated:
                _ = cSrv.hardDeleteChannelById(channelCreated.channelId)

            return render_template("base/error.html")
    
    try:
        cSrv: ChannelService = ChannelService(userId=session.get("userId"))
        channel: Channel | None = cSrv.doIAlreadyHaveChannel()
        if channel:
            return redirect(url_for("channel_details.channel_detail", channel_id=channel.channelId))
    except ServiceException as e:
        #TODO: LOGGING
        return render_template("base/error.html", error=str(e))
    except Exception as e:
        #TODO: LOGGING
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

            return redirect(url_for("channel_details.channel_detail", channel_id=channelUpdated.channelId))
        except ServiceException as e:
            #TODO: LOGGING
            return render_template("base/error.html", error=str(e))
        except Exception as e:
            #TODO: LOGGING
            return render_template("base/error.html")

    try:
        return render_template("channel/channel_details_edit.html", ch=channel)
    except Exception as e:
        #TODO: Logging
        return render_template("base/error.html")

#
# API
#
@channelDetailsBp.route("/channel/videos/list/<int:channel_id>/<int:page>")
@loginRequired
def channel_list_videos_pagination(channel_id: int, page: int):
    
    try:
        vs = VideoService(userId=session.get("userId"), channelId=channel_id)

        if (user:=cast(dict[str, object] | None, session.get("user", None))) is None:
            #TODO: Logging: user doesn't exists
            #This cannot happen
            raise Exception("User is not in session")

        userOwnChannel = channel_id == user.get("channelId", 0)

        channelsUserSubscribed = nredis.client.get(
            USER_SUBSCRIBED_CHANNELS_KEY.format(userId=session.get("userId"))
        )
        
        isSubscribed = False
        if channelsUserSubscribed:
            channelsUserSubscribed = cast(ChannelSubscribedList, json.loads(channelsUserSubscribed))
            isSubscribed = any(True for channel in channelsUserSubscribed if channel.get("channelId", 0) == channel_id)

        channelVideos, _ = vs.selectLimitProcessedVideosByChannelId(
            limit=LIMIT_VIDEOS_CHANNEL,
            page=page,
            userOwnVideoChannel=userOwnChannel,
            userIsSubscribedToChannel=isSubscribed
        )

        return jsonify({"videos": channelVideos})
    except ServiceException as e:
        #TODO: Logging
        return jsonify({"videos": []})
    except Exception as e:
        #TODO: Logging
        return jsonify({"videos": []})
