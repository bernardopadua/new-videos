# BUILT-IN
from dataclasses import dataclass, field

# TYPING
from typing import Type

# ENTITY
from nvideos_web.core.entity.base.base_entity import (
    MetadataClass, BaseMetadataAuditMixin,
    ModelField, AuditData, BaseModelData,
    BaseInput
)

@dataclass(frozen=True, slots=True)
class Channel(AuditData, BaseModelData):
    channelId: int = field(default=0)
    channelName: str = field(default="")
    channelDescription: str = field(default="")
    channelImageUrl: str = field(default="")
    channelAvatarUrl: str = field(default="")
    channelIsActive: bool = field(default=False)
    userId: int = field(default=0)

@dataclass
class ChannelInput(BaseInput):
    channelName: str | None = field(default=None)
    channelDescription: str | None = field(default=None)
    channelImageUrl: str | None = field(default=None)
    channelAvatarUrl: str | None = field(default=None)
    channelIsActive: bool | None = field(default=None)
    userId: int | None = field(default=None)

class ChannelMetadata(
    MetadataClass[Channel],
    BaseMetadataAuditMixin
):
    _table_name: str = "channel"
    _model_data: type[Channel] = Channel
    _use_prefix: str = "ch"
    #Columns
    channelId: ModelField = ModelField("channel_id")
    channelName: ModelField = ModelField("channel_name")
    channelDescription: ModelField = ModelField("channel_description")
    channelImageUrl: ModelField = ModelField("channel_image_url")
    channelAvatarUrl: ModelField = ModelField("channel_avatar_url")
    channelIsActive: ModelField = ModelField("channel_is_active")
    userId: ModelField = ModelField("user_id")
