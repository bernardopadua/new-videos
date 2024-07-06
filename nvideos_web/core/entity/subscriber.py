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
class Subscriber(AuditData, BaseModelData):
    subscriberId: int = field(default=0)
    channelId: int = field(default=0)
    userId: int = field(default=0)
    subscriberIsActive: bool = field(default=False)

@dataclass
class SubscriberInput(BaseInput):
    subscriberId: int | None = field(default=None)
    channelId: int | None = field(default=None)
    userId: int | None = field(default=None)
    subscriberIsActive: bool | None = field(default=None)

class SubscriberMetadata(
    MetadataClass[Subscriber],
    BaseMetadataAuditMixin
):
    _table_name: str = "subscriber"
    _model_data: Type[Subscriber] = Subscriber
    _use_prefix: str = "su"
    #Columns
    subscriberId: ModelField = ModelField("subscriber_id")
    channelId: ModelField = ModelField("channel_id")
    userId: ModelField = ModelField("user_id")
    subscriberIsActive: ModelField = ModelField("subscriber_is_active")
