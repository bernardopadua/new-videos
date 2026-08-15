# TYPING
from typing import Self, override, final

# DATACLASS
from dataclasses import asdict

# ENTITY
from nvideos_web.core.entity.comment import (
    Comment, CommentInput, CommentList
)

# REPOSITORY
from nvideos_web.core.repository.comment import CommentRepository

# SERVICES
from nvideos_web.impl.comment_repository import PgCommentRepository
from nvideos_web.services.base.service import BaseService

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# ERRORS
from nvideos_web.services.base.error import InputDataIsNone
from nvideos_web.services.comment.error import CommentNoCurrentUser

@final
class CommentService(BaseService[CommentInput]):
    def __init__(
        self, 
        *,
        userId: int | None = None, 
        dbContext: type[NewVideosDBContext] | None = None
    ) -> None:
        super().__init__(currentUser=userId)
        #mypy doesn't understand inline if
        if dbContext is None:
            dbContext=NewVideosDBContext

        self._cmRep: PgCommentRepository = PgCommentRepository(dbContext=dbContext)

    def selectCommentsFromVideoKey(self, videoKey: str) -> tuple[list[dict[str, object]], int]:
        comments, totalComments = self._cmRep.selectByVideoKey(videoKey)
        return [ comment.toJson() for comment in comments ], totalComments

    def selectChildCommentsFromCommentId(self, commentId: int) -> list[dict[str, object]]:
        comments = self._cmRep.selectChildCommentsByParentCommentId(commentId)
        return [ comment.toJson() for comment in comments ]

    @override
    def checkIdExists(self, idRegistry: int) -> Self:
        self._checkExists = self._cmRep.checkIdExists(idRegistry)
        return self

    @override
    def getInputData(self) -> CommentInput:
        if self._filledInputData is None:
            raise InputDataIsNone(InputDataIsNone.genericError())

        return self._filledInputData

    def replyComment(self, 
        videoId: int, 
        comment: str, 
        userName: str,
        userAvatarUrl: str,
        /, *, 
        commentId: int | None = None
    ) -> CommentList:
        if not self.currentUser:
            raise CommentNoCurrentUser("You must be logged in to reply to a comment")
        
        self.insertingMode()
        inputData = self.fillInputData(
            videoId=videoId, 
            comment=comment, 
            userId=self.currentUser, 
            commentId=commentId
        ).getInputData()
        auditData = self.fillAuditData().getAuditData()

        dbComment = self._cmRep.create(inputData, auditData)

        return CommentList(
            commentId=dbComment.commentId,
            createdAt=dbComment.createdAt,
            commentCommentId=dbComment.commentCommentId,
            commentDescription=dbComment.commentDescription, 
            totalRecomments=0, 
            userId=dbComment.userId, 
            userName=userName,
            userAvatarUrl=userAvatarUrl
        )


    @override
    def fillInputData(self, /, *, 
        videoId: int | None = None, 
        comment: str | None = None,
        userId: int | None = None,
        commentId: int | None = None
    ) -> Self:

        self._filledInputData = CommentInput(
            videoId=videoId,
            commentDescription=comment,
            userId=userId,
            commentCommentId=commentId,
        )
        return self