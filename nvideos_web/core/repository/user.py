# BUILT-IN
from abc import ABC, abstractmethod

from nvideos_web.core.entity.user import (
    User,
    UserInput
)
from nvideos_web.core.entity.base.base_entity import AuditData

class UserRepository(ABC):
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
    @abstractmethod
    def selectByUserName(self, userName: str) -> User:
        ...
    @abstractmethod
    def selectByUserEmail(self, userEmail: str) -> User:
        ...
    @abstractmethod
    def selectByUserId(self, userId: int) -> User:
        ...
    @abstractmethod
    def userEmailExists(self, userEmail: str) -> bool: 
        ...

class UserPasswordHasher(ABC):
    @abstractmethod
    def hashPassword(self, password: str) -> str:
        ...