from datetime import date
from dataclasses import dataclass, field
from typing import Any, Optional

from nvideos_web.core.entity.constants import UserPermissions
from nvideos_web.core.entity.entity_base import BaseFieldsMixin

@dataclass
class User(BaseFieldsMixin):
    userId: int
    userName: str
    userSurname: str
    userEmail: str
    userPassword: str = field(repr=False, hash=False)
    userBirthDate: date
    userAvatarUrl: str
    userPermission: int
    userIsActive: bool

@dataclass(frozen=True)
class NewUserInput:
    userName: str
    userSurname: str
    userEmail: str
    userPassword: str
    userBirthDate: date = None
    userAvatarUrl: str = field(default="")
    userPermission: int = field(default=UserPermissions.P_COMMOM_USER.value)
    userIsActive: Optional[bool] = field(default=True)
