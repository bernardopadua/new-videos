from dataclasses import dataclass, field
from typing import TypeVar

from nvideos_web.core.entity.base_entity import (
    MetadataClass,
    ModelField
)

@dataclass(frozen=True, slots=True)
class UserPermission:
    userPermission: bytes = field(default=bytes(0))
    permissionDescription: str = field(default="")

class UserPermissionMetadata(MetadataClass):
    _table_name: str = "user_permission"
    _model_data: UserPermission | None = None #Stored after definition
    _use_prefix: str = "up"
    #Columns
    userPermission: ModelField = ModelField("user_permission")
    permissionDescription: ModelField = ModelField("permission_description")
