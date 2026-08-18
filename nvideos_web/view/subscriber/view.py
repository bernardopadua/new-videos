# FLASK
from flask import (
    Blueprint, session, jsonify, 
    request as flaskRequest
)

# DB
from nvideos_web.db.redis import nredis

# DECORATORS
from nvideos_web.services.base.error import ServiceException
from nvideos_web.services.channel.service import ChannelService
from nvideos_web.view.endpoint_decorators import loginRequired

# SERVICE
from nvideos_web.services.subscriber.service import SubscriberService

# TEMPLATE GLOBAL
from nvideos_web.view.template_context import getChannelSubscriberDescription

subscriberBp = Blueprint(
    "subscriber", __name__
)

#
# API
#

@subscriberBp.route("/channel/<int:channel_id>/total-subscribers", methods=["GET"])
@loginRequired
def total_subscribed_channel(channel_id: int):
    sSrv: SubscriberService = SubscriberService(userId=session.get("userId"))
    try:
        totalSubscribers = sSrv.selectTotalSubscribers(channel_id)
        descriptionSubscribers = getChannelSubscriberDescription(totalSubscribers) + " subscribers"
    except ServiceException as e:
        return jsonify({"totalSubscribers": None, "error": str(e)})
    except Exception:
        return jsonify({"error": "Error getting total subscribers."})

    return jsonify({"totalSubscribers": descriptionSubscribers})

@subscriberBp.route("/channel/<int:channel_id>/subscribed", methods=["GET"])
@loginRequired
def is_subscribed_channel(channel_id: int):
    sSrv: SubscriberService = SubscriberService(userId=session.get("userId"))
    cSrv: ChannelService = ChannelService(userId=session.get("userId"))
    
    try:
        if not cSrv.checkIdExists(channel_id).getCheckIdExists():
            return jsonify({"isSubscribed": False})

        return jsonify({"isSubscribed": sSrv.checkAlreadySubscribed(channel_id)})
    except ServiceException as e:
        return jsonify({"isSubscribed": False, "error": str(e)})
    except Exception as e:
        return jsonify({"isSubscribed": False})

@subscriberBp.route("/channel/<int:channel_id>/subscribe", methods=["POST"])
@loginRequired
def subscribe_channel(channel_id: int):
    import json
    from nvideos_web.db.redis_constants import USER_SUBSCRIBED_CHANNELS_KEY
    
    sSrv: SubscriberService = SubscriberService(userId=session.get("userId"))
    cSrv: ChannelService = ChannelService(userId=session.get("userId"))

    try:
        if not cSrv.checkIdExists(channel_id).getCheckIdExists():
            return jsonify({"isSubscribed": False})

        userSubscribed = sSrv.checkSubscribedAndSubscribe(channel_id)

        if (userSubscribed is None or 
            not userSubscribed.subscriber.subscriberIsActive):
            #TODO: Logging
            return jsonify({"isSubscribed": False})

        channel = cSrv.selectChannelById(channel_id)
        channelsSubscribed = nredis.client.get(USER_SUBSCRIBED_CHANNELS_KEY.format(userId=sSrv.currentUser))

        if channel is None:
            #TODO: LOG: Logging
            return jsonify({"isSubscribed": False})

        if channelsSubscribed is None:
            channelsSubscribed = [{
                "channelId": channel.channelId,
                "channelAvatarUrl": channel.channelAvatarUrl,
                "channelName": channel.channelName
            }]
        else:
            if not isinstance(channelsSubscribed, (str, bytes)):
                #TODO: LOG: Logging
                raise Exception("Result from redis is not JSON string/bytes.")

            channelsSubscribed = json.loads(channelsSubscribed)
            
            if not isinstance(channelsSubscribed, list):
                #TODO: LOG: Logging
                raise Exception("Result from redis is not a list.")

            channelsSubscribed.append({
                "channelId": channel.channelId,
                "channelAvatarUrl": channel.channelAvatarUrl,
                "channelName": channel.channelName
            })

        #I'm just assuming
        redisIsSet = nredis.client.set(
            USER_SUBSCRIBED_CHANNELS_KEY.format(userId=sSrv.currentUser),
            json.dumps(channelsSubscribed)
        )

        #I would comment the lines below, but I will keep this to avoid deleting commented code.
        if not redisIsSet:
            #TODO: Logging
            pass      

        return jsonify({"isSubscribed": True})
    except ServiceException as e:
        return jsonify({"isSubscribed": False, "error": str(e)})
    except Exception as e:
        return jsonify({"isSubscribed": False})

@subscriberBp.route("/channel/<int:channel_id>/unsubscribe", methods=["POST"])
@loginRequired
def unsubscribe_channel(channel_id: int):
    sSrv: SubscriberService = SubscriberService(userId=session.get("userId"))
    cSrv: ChannelService = ChannelService(userId=session.get("userId"))

    try:
        if not cSrv.checkIdExists(channel_id).getCheckIdExists():
            return jsonify({"isSubscribed": False})

        isUnsubscribed = sSrv.checkSubscribedAndUnsubscribe(channel_id)

        return jsonify({"isUnsubscribed": isUnsubscribed})
    except ServiceException as e:
        return jsonify({"isUnsubscribed": False, "error": str(e)})
    except Exception as e:
        return jsonify({"isUnsubscribed": False})
