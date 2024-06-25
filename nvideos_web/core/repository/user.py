from typing import Protocol
from abc import abstractmethod

from nvideos_web.core.entity.user import User

class UserRepository(Protocol):
    @abstractmethod
    def create(self, userData: User) -> User:
        raise NotImplementedError()
    
    @abstractmethod
    def update(self, userData: User, newUserData: User) -> User:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, userId: int) -> None:
        raise NotImplementedError()

class UserPasswordHasher(Protocol):
    @abstractmethod
    def hashPassword(self, password: str) -> str:
        raise NotImplementedError()