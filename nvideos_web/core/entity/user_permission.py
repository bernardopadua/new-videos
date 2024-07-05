from dataclasses import dataclass, field
from typing import Type

from nvideos_web.core.entity.base.base_entity import (
    MetadataClass,
    ModelField
)

@dataclass(frozen=True, slots=True)
class UserPermission:
    userPermission: str = field(default="")
    permissionDescription: str = field(default="")

class UserPermissionMetadata(MetadataClass[UserPermission]):
    _table_name: str = "user_permission"
    _model_data: Type[UserPermission] = UserPermission
    _use_prefix: str = "up"
    #Columns
    userPermission: ModelField = ModelField("user_permission")
    permissionDescription: ModelField = ModelField("permission_description")
