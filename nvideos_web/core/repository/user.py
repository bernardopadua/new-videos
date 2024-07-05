from typing import Protocol
from abc import abstractmethod

from nvideos_web.core.entity.user import (
    User,
    UserInput
)
from nvideos_web.core.entity.base.base_entity import AuditData

class UserRepository(Protocol):
    @abstractmethod
    def create(self, userInputData: UserInput, auditInputData: AuditData) -> User: 
        ...
    @abstractmethod
    def checkIdExists(self, userId: int) -> bool: 
        ...
    @abstractmethod
    def updateById(self, userId: int, newUserData: UserInput, auditData: AuditData) -> User: 
        ...
    @abstractmethod
    def delete(self, userId: int, auditData: AuditData) -> User: 
        ...

class UserPasswordHasher(Protocol):
    @abstractmethod
    def hashPassword(self, password: str) -> str:
        ...