# FLASK
from flask import (
    Blueprint, session, jsonify, 
    request as flaskRequest
)

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
    #static_folder="static", static_url_path="/user_details/static",
    #template_folder="template"
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
    sSrv: SubscriberService = SubscriberService(userId=session.get("userId"))
    cSrv: ChannelService = ChannelService(userId=session.get("userId"))

    try:
        if not cSrv.checkIdExists(channel_id).getCheckIdExists():
            return jsonify({"isSubscribed": False})

        sSrv.checkSubscribedAndSubscribe(channel_id)

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
