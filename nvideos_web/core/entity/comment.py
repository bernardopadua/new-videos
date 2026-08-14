# BUILT-IN
from dataclasses import dataclass, field
from typing import final

# ENTITY
from nvideos_web.core.entity.base.base_entity import (
    AuditData, BaseModelData, BaseInput, ModelField,
    MetadataClass, BaseMetadataAuditMixin
)

@dataclass(frozen=True, slots=True)
class Comment(AuditData, BaseModelData):
    commentId: int = field(default=0)
    videoId: int = field(default=0)
    userId: int = field(default=0)
    commentDescription: str = field(default="")
    commentCommentId: int | None = field(default=None)

@dataclass
class CommentInput(BaseInput):
    videoId: int | None = field(default=None)
    userId: int | None = field(default=None)
    commentDescription: str | None = field(default=None)
    commentCommentId: int | None = field(default=None)

@dataclass(frozen=True, slots=True)
class CommentList(Comment):
    userName: str = field(default="")
    userAvatarUrl: str = field(default="")
    totalRecomments: int = field(default=0)

@final
class CommentMetadata(
    MetadataClass[Comment],
    BaseMetadataAuditMixin
):
    _table_name = "nvideo_comment"
    _model_data = Comment
    _use_prefix = "cc"
    #Columns
    commentId: ModelField = ModelField("comment_id")
    videoId: ModelField = ModelField("video_id")
    userId: ModelField = ModelField("user_id")
    commentDescription: ModelField = ModelField("comment_description")
    commentCommentId: ModelField = ModelField("comment_comment_id")
