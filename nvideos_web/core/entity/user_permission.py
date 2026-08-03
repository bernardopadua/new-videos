# BUILT-IN
from dataclasses import dataclass, field

# TYPING
from typing import final

# ENTITY
from nvideos_web.core.entity.base.base_entity import (
    MetadataClass,
    ModelField
)

@dataclass(frozen=True, slots=True)
class UserPermission:
    userPermission: str = field(default="")
    permissionDescription: str = field(default="")

@final
class UserPermissionMetadata(MetadataClass[UserPermission]):
    _table_name = "user_permission"
    _model_data = UserPermission
    _use_prefix = "up"
    #Columns
    userPermission: ModelField = ModelField("user_permission")
    permissionDescription: ModelField = ModelField("permission_description")
