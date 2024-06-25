from datetime import date
from dataclasses import dataclass, field
from typing import Any, Optional

from nvideos_web.core.entity.metadata import setUpField, setUpMetadata
from nvideos_web.core.entity.constants import UserPermissions
from nvideos_web.core.entity.entity_base import BaseFieldsMixin

@dataclass
class User(BaseFieldsMixin):
    userId: int = setUpField("user_id")
    userName: str = setUpField("user_name")
    userSurname: str = setUpField("user_surname")
    userEmail: str = setUpField("user_email")
    userPassword: str = field(repr=False, hash=False, metadata=setUpMetadata("user_password"))
    userBirthDate: date = setUpField("user_birth_date")
    userAvatarUrl: str = setUpField("user_avatar_url")
    userPermission: int = setUpField("user_permission")
    userIsActive: bool = setUpField("user_is_active")

@dataclass(frozen=True)
class NewUserInput:
    userName: str = setUpField("user_name")
    userSurname: str = setUpField("user_surname")
    userEmail: str = setUpField("user_email")
    userPassword: str = setUpField("user_password")
    userBirthDate: date = setUpField("user_birth_date", default=UserPermissions.P_COMMOM_USER.value)
    userAvatarUrl: str = setUpField("user_avatar_url", default="") 
    userPermission: int = setUpField("user_permission", default=UserPermissions.P_COMMOM_USER.value) 
    userIsActive: Optional[bool] = setUpField("user_is_active", default=True) 
