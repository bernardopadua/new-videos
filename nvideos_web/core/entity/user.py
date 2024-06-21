from datetime import datetime
from dataclasses import dataclass

@dataclass
class UserData:
    id: int
    name: str
    surname: str
    email: str
    birth_date: datetime

class User:
    def __init__(self) -> None:
        self.__
        pass