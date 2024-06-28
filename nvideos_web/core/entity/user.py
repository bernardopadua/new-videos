from datetime import date
from dataclasses import dataclass, field
from typing import Any, Optional

from nvideos_web.core.entity.metadata import setUpField, setUpMetadata
from nvideos_web.core.entity.constants import UserPermissions
from nvideos_web.core.entity.entity_base import BaseMetadata, ModelField, modelMetadataMapper

@modelMetadataMapper
class UserMetadata(BaseMetadata):
    __table_name__: str = "nvideo_user"
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

print(UserMetadata.userPermission.owner)

@dataclass(frozen=True, slots=True)
class User:
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
    userPermission: int = setUpField(UserMetadata.userPermission, default=0)
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
