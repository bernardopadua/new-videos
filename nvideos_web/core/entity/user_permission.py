from dataclasses import dataclass
from typing import Optional

from nvideos_web.core.entity.base_entity import (
    modelMetadataMapper,
    BaseMetadataUtilMixin,
    ModelField
)

from nvideos_web.core.entity.metadata import setUpField

@modelMetadataMapper
class UserPermissionMetadata(BaseMetadataUtilMixin):
    __table_name__: str = "user_permission"
    __model_data__: Optional["UserPermission"] = None #Stored after definition
    __use_prefix__: str = "up"
    #Columns
    userPermission: ModelField = ModelField("user_permission")
    permissionDescription: ModelField = ModelField("permission_description")

@dataclass(frozen=True, slots=True)
class UserPermission:
    userPermission: bytes = setUpField(UserPermissionMetadata.userPermission, default=bytes(0))
    permissionDescription: str = setUpField(UserPermissionMetadata.permissionDescription, default="")


UserPermissionMetadata.__model_data__ = UserPermission