# BUILT-IN
from abc import ABC, abstractmethod

# ENTITY
from nvideos_web.core.entity.comment import (
    Comment, CommentInput, CommentList
)

from nvideos_web.core.entity.base.base_entity import AuditData

class CommentRepository(ABC):
    @abstractmethod
    def selectByVideoKey(self, videoKey: str) -> list[CommentList]:
        ...
    @abstractmethod
    def selectChildCommentsByParentCommentId(self, parentCommentId: int) -> list[CommentList]:
        ...
    @abstractmethod
    def selectById(self, commentId: int) -> Comment | None:
        ...
    @abstractmethod
    def create(self, commentInputData: CommentInput, auditInputData: AuditData) -> Comment: 
        ...
    @abstractmethod
    def checkIdExists(self, commentId: int) -> bool: 
        ...
    @abstractmethod
    def updateById(self, commentId: int, newCommentData: CommentInput, auditData: AuditData) -> Comment: 
        ...
    @abstractmethod
    def delete(self, commentId: int, auditData: AuditData) -> Comment: 
        ...