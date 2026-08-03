# BUILT-IN
from dataclasses import dataclass, field
from typing import final

# ENTITY
from nvideos_web.core.entity.base.base_entity import (
    AuditData, BaseModelData, BaseInput, ModelField,
    MetadataClass, BaseMetadataAuditMixin
)

@dataclass(frozen=True, slots=True)
class Video(AuditData, BaseModelData):
    videoId: int = field(default=0)
    videoTitle: str = field(default="")
    videoDescription: str = field(default="")
    videoTimeDuration: int = field(default=0)
    videoViewCount: int = field(default=0)
    videoThumbUrl: str = field(default="")
    videoTags: list[str] = field(default_factory=list)
    videoPermission: str = field(default="")
    channelId: int = field(default=0)
    userId: int = field(default=0)
    videoKey: str = field(default="")

@dataclass
class VideoInput(BaseInput):
    videoTitle: str | None = field(default=None)
    videoDescription: str | None = field(default=None)
    videoTimeDuration: int | None = field(default=None)
    videoViewCount: int | None = field(default=None)
    videoThumbUrl: str | None = field(default=None)
    videoTags: list[str] | None = field(default=None)
    videoPermission: str | None = field(default=None)
    channelId: int | None = field(default=None)
    userId: int | None = field(default=None)
    videoKey: str | None = field(default=None)

@final
class VideoMetadata(
    MetadataClass[Video],
    BaseMetadataAuditMixin
):
    _table_name = "nvideo_video"
    _model_data = Video
    _use_prefix = "vv"
    #Columns
    videoId: ModelField = ModelField("video_id")
    videoTitle: ModelField = ModelField("video_title")
    videoDescription: ModelField = ModelField("video_description")
    videoTimeDuration: ModelField = ModelField("video_time_duration")
    videoViewCount: ModelField = ModelField("video_view_count")
    videoThumbUrl: ModelField = ModelField("video_thumb_url")
    videoTags: ModelField = ModelField("video_tags")
    videoPermission: ModelField = ModelField("video_permission")
    channelId: ModelField = ModelField("channel_id")
    userId: ModelField = ModelField("user_id")
    videoKey: ModelField = ModelField("video_key")