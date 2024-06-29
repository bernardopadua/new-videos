from datetime import date
from dataclasses import dataclass, field
from typing import Optional

from nvideos_web.core.entity.metadata import setUpField, setUpMetadata
from nvideos_web.core.entity.constants import UserPermissions
from nvideos_web.core.entity.base_entity import (
    BaseMetadataAuditMixin, BaseModelData,
    BaseMetadataUtilMixin, ModelField, 
    modelMetadataMapper
)

@modelMetadataMapper
class UserMetadata(BaseMetadataAuditMixin, BaseMetadataUtilMixin):
    __table_name__: str = "nvideo_user"
    __model_data__: Optional["User"] = None #Stored after definition
    __use_prefix__: str = "uu"
    #Columns
    userId: ModelField = ModelField("user_id")
    userName: ModelField = ModelField("user_name")
    userSurname: ModelField = ModelField("user_surname")
    userEmail: ModelField = ModelField("user_email")
    userPassword: ModelField = ModelField("user_password")
    userBirthDate: ModelField = ModelField("user_birth_date")
    userAvatarUrl: ModelField = ModelField("user_avatar_url")
    userPermission: ModelField = ModelField("user_permission")
    userIsActive: ModelField = ModelField("user_is_active")

@dataclass(frozen=True, slots=True)
class User(BaseModelData):
    userId: int = setUpField(UserMetadata.userId, default=0)
    userName: str = setUpField(UserMetadata.userName, default="")
    userSurname: str = setUpField(UserMetadata.userSurname, default="")
    userEmail: str = setUpField(UserMetadata.userEmail, default="")
    userPassword: str = field(repr=False, hash=False, 
        metadata=setUpMetadata(UserMetadata.userPassword),
        default=""
    )
    userBirthDate: Optional[date] = setUpField(UserMetadata.userBirthDate, default=None)
    userAvatarUrl: str = setUpField(UserMetadata.userAvatarUrl, default="")
    userPermission: bytes = setUpField(UserMetadata.userPermission, default=bytes(0))
    userIsActive: bool = setUpField(UserMetadata.userIsActive, default=True)

@dataclass
class UserInput:
    userName: str = setUpField(UserMetadata.userName)
    userSurname: str = setUpField(UserMetadata.userSurname)
    userEmail: str = setUpField(UserMetadata.userEmail)
    userPassword: str = setUpField(UserMetadata.userPassword)
    userBirthDate: date = setUpField(UserMetadata.userBirthDate, default_factory=date.today)
    userAvatarUrl: str = setUpField(UserMetadata.userAvatarUrl, default="") 
    userPermission: bytes = setUpField(UserMetadata.userPermission, default=UserPermissions.P_COMMOM_USER.value) 
    userIsActive: Optional[bool] = setUpField(UserMetadata.userIsActive, default=True) 

#Storing into metadata object the reference to User value-object
UserMetadata.__model_data__ = User