from typing import Protocol
from abc import abstractmethod

from nvideos_web.core.entity.user import (
    User,
    UserInput
)
from nvideos_web.core.entity.base_entity import AuditData

class UserRepository(Protocol):
    @abstractmethod
    def create(self, userInputData: UserInput, auditInputData: AuditData) -> User:
        raise NotImplementedError()
    
    @abstractmethod
    def updateById(self, userId: int, newUserData: UserInput, auditData: AuditData) -> User:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, userId: int) -> None:
        raise NotImplementedError()

class UserPasswordHasher(Protocol):
    @abstractmethod
    def hashPassword(self, password: str) -> str:
        raise NotImplementedError()