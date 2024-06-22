from datetime import datetime
from dataclasses import dataclass

from nvideos_web.core.entity.entity_base import BaseFieldsMixin

@dataclass
class User(BaseFieldsMixin):
    id: int
    name: str
    surname: str
    email: str
    birth_date: datetime

class User:
    def __init__(self, data: User) -> None:
        self.d = data
        pass