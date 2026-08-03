# BUILT-IN
from datetime import date
from dataclasses import dataclass, field

# TYPING
from typing import final

# ENTITY
from nvideos_web.core.entity.base.base_entity import (
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
    userName: str | None = field(default=None)
    userSurname: str | None = field(default=None)
    userEmail: str | None = field(default=None)
    userPassword: str | None = field(default=None)
    userBirthDate: date | None = field(default=None)
    userAvatarUrl: str | None = field(default=None)
    userPermission: str | None = field(default=None)
    userIsActive: bool | None = field(default=None)

@final
class UserMetadata(
    MetadataClass[User],
    BaseMetadataAuditMixin
):
    _table_name = "nvideo_user"
    _model_data = User
    _use_prefix = "uu"
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
