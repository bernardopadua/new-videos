# FLASK
from flask import (
    Blueprint, session, jsonify, 
    request as flaskRequest
)

# TYPING
from typing import cast

# DECORATORS
from nvideos_web.services.base.error import ServiceException
from nvideos_web.view.endpoint_decorators import loginRequired

# SERVICE
from nvideos_web.services.comment.service import CommentService

commentBp = Blueprint(
    "comment", __name__
)

#
# API
#

@commentBp.route("/comment/load/replies/<int:comment_id>", methods=["GET"])
@loginRequired
def load_replies(comment_id: int):
    cSrv: CommentService = CommentService(userId=session.get("userId"))
    replies = cSrv.selectChildCommentsFromCommentId(comment_id)
    return jsonify(replies)

@commentBp.route("/comment/reply/<int:video_id>", methods=["POST"])
@commentBp.route("/comment/reply/<int:video_id>/<int:parent_comment_id>", methods=["POST"])
@loginRequired
def reply(video_id: int, parent_comment_id: int | None = None):
    cSrv: CommentService = CommentService(userId=session.get("userId"))
    
    user = session.get("user")
    if not user:
        return jsonify({}), 400

    data = flaskRequest.get_json() or {}
    comment = cast(str, data.get("comment")) or None
    if not comment:
        return jsonify({"error": "Comment is required"}), 400

    try:
        userName: str = user["userName"]
        userAvatarUrl: str = user["userAvatarUrl"]

        commentList = cSrv.replyComment(
            video_id,
            comment,
            userName,
            userAvatarUrl,
            commentId=parent_comment_id
        )
        return jsonify({"success": True, "comments": [commentList.toJson()]})
    except ServiceException as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        #TODO: LOG: Loggging e
        return jsonify({}), 400
