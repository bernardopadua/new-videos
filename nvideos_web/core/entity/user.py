# BUILT-IN
from datetime import date
from dataclasses import dataclass, field

# TYPING
from typing import Type, TypeVar

# ENTITY
from nvideos_web.core.entity.base_entity import (
    MetadataClass, BaseMetadataAuditMixin,
    ModelField, AuditData, BaseModelData,
    BaseInput
)

@dataclass(frozen=True, slots=True)
class User(AuditData, BaseModelData):
    userId: int = field(default=0)
    userName: str = field(default="")
    userSurname: str = field(default="")
    userEmail: str = field(default="")
    userPassword: str = field(repr=False, hash=False, default="")
    userBirthDate: date | None = field(default=None)
    userAvatarUrl: str = field(default="")
    userPermission: bytes = field(default=bytes(0))
    userIsActive: bool = field(default=True)

@dataclass
class UserInput(BaseInput):
    userName: str | None
    userSurname: str | None
    userEmail: str | None
    userPassword: str | None
    userBirthDate: date | None
    userAvatarUrl: str | None 
    userPermission: str | None 
    userIsActive: bool | None

class UserMetadata(
    MetadataClass[User],
    BaseMetadataAuditMixin
):
    _table_name: str = "nvideo_user"
    _model_data: Type[User] = User
    _use_prefix: str = "uu"
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

# @dataclass(frozen=True, slots=True)
# class User:
#     userId: int = setUpField(UserMetadata.userId, default=0)
#     userName: str = setUpField(UserMetadata.userName, default="")
#     userSurname: str = setUpField(UserMetadata.userSurname, default="")
#     userEmail: str = setUpField(UserMetadata.userEmail, default="")
#     userPassword: str = field(repr=False, hash=False, 
#         metadata=setUpMetadata(UserMetadata.userPassword),
#         default=""
#     )
#     userBirthDate: Optional[date] = setUpField(UserMetadata.userBirthDate, default=None)
#     userAvatarUrl: str = setUpField(UserMetadata.userAvatarUrl, default="")
#     userPermission: bytes = setUpField(UserMetadata.userPermission, default=bytes(0))
#     userIsActive: bool = setUpField(UserMetadata.userIsActive, default=True)

# @dataclass
# class UserInput:
#     userName: str = setUpField(UserMetadata.userName)
#     userSurname: str = setUpField(UserMetadata.userSurname)
#     userEmail: str = setUpField(UserMetadata.userEmail)
#     userPassword: str = setUpField(UserMetadata.userPassword)
#     userBirthDate: date = setUpField(UserMetadata.userBirthDate, default_factory=date.today)
#     userAvatarUrl: str = setUpField(UserMetadata.userAvatarUrl, default="") 
#     userPermission: bytes = setUpField(UserMetadata.userPermission, default=UserPermissions.P_COMMOM_USER.value) 
#     userIsActive: Optional[bool] = setUpField(UserMetadata.userIsActive, default=True) 

#Storing into metadata object the reference to User value-object
#UserMetadata._model_data= User