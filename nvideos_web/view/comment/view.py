# FLASK
from flask import (
    Blueprint, session, jsonify, 
    request as flaskRequest
)

# DECORATORS
from nvideos_web.services.base.error import ServiceException
from nvideos_web.view.endpoint_decorators import loginRequired

# SERVICE
from nvideos_web.services.comment.service import CommentService

commentBp = Blueprint(
    "comment", __name__
)

@commentBp.route("/comment/load/replies/<int:comment_id>", methods=["GET"])
@loginRequired
def load_replies(comment_id: int):
    service: CommentService = CommentService(userId=session.get("userId"))
    replies = service.selectChildCommentsFromCommentId(comment_id)
    return jsonify(replies)